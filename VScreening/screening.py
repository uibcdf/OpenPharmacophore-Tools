import openpharmacophore as oph
from openpharmacophore.algorithms.alignment import apply_radii_to_bounds, transform_embeddings

from rdkit import Chem, RDConfig
from rdkit.Chem import ChemicalFeatures, rdDistGeom
from rdkit.Chem.Pharm3D import EmbedLib

from collections import namedtuple
from multiprocessing import Pool, Queue, Manager, Value
import os
from operator import itemgetter

Match = namedtuple("Match", ["score", "id", "mol"])
featFactory = ChemicalFeatures.BuildFeatureFactory(os.path.join(RDConfig.RDDataDir,
                                                                     'BaseFeatures.fdef'))

def get_rdkit_pharmacophore(pharmacophore):
    """ Transfor a pharmacophore to an rdkit pharmacophore
    
        Parameters
        ----------
        pharmacophore : openpharmacophore.Pharmacophore
            The pharmacophore.
    """
    
    rdkit_pharmacophore, radii = pharmacophore.to_rdkit()
    apply_radii_to_bounds(radii, rdkit_pharmacophore)

    return rdkit_pharmacophore
        
def align_molecule(mol, matches, rdkit_pharmacophore):
    """Align a molecule to a given pharmacophore.
    
    Uses rdkit alignment algorithm

    Parameters
    ----------
    mol : rdkit.Chem.mol
        Molecule to align.
        
    matches : list
        If a moleculed is matched to the pharmacophore it will be appended to
        this list
        
    rdkit_pharmacophore : 
        An rdkit pharmacophore

    """
    
    bounds_matrix = rdDistGeom.GetMoleculeBoundsMatrix(mol)
    # Check if the molecule features can match with the pharmacophore.
    can_match, all_matches = EmbedLib.MatchPharmacophoreToMol(mol, featFactory, rdkit_pharmacophore)
    # all_matches is a list of tuples where each tuple contains the chemical features
    if can_match:
        # Match the molecule to the pharmacophore without aligning it
        failed, bounds_matrix_matched, matched_mols, match_details = EmbedLib.MatchPharmacophore(all_matches, 
                                                                                        bounds_matrix,
                                                                                        rdkit_pharmacophore, 
                                                                                        useDownsampling=True)
        if failed:
            return
    else:
        return
    atom_match = [list(x.GetAtomIds()) for x in matched_mols]
    try:
        mol_H = Chem.AddHs(mol)
        # Embed molecule onto the pharmacophore
        # embeddings is a list of molecules with a single conformer
        b_matrix, embeddings, num_fail = EmbedLib.EmbedPharmacophore(mol_H, atom_match, rdkit_pharmacophore, count=10)
    except:
        return
    # Align embeddings to the pharmacophore 
    SSDs = transform_embeddings(rdkit_pharmacophore, embeddings, atom_match)
    if len(SSDs) == 0:
        return
    best_fit_index = min(enumerate(SSDs), key=itemgetter(1))[0]
    try:
        mol_id = mol.GetProp("_Name")
    except:
        mol_id = None

    matched_mol = Match(SSDs[best_fit_index], mol_id, embeddings[best_fit_index])
    # Append to list in ordered manner
    matches.append(matched_mol)
    
def get_files(path):
    """ List all files from a directory and put them in a queue.
    
        Parameters
        ----------
        path : str
            The path of the files.
        
        Returns
        -------
        file_queue : multiprocessing.Queue
            The file queue.
    """
    exclude_prefixes = ('__', '.')
    
    file_queue = Queue()
    for root, dirs, files in os.walk(path):
        # Ignore hidden folders and files
        files = [f for f in files if not f.startswith(exclude_prefixes)]
        dirs[:] = [d for d in dirs if not d.startswith(exclude_prefixes)]
        for file in files:
            file_queue.put(os.path.join(root, file))
    
    return file_queue

                
def screen_files(file_queue, matches, n_molecules, pharmacophore):
    """ Perform virtual screening to a queue of files.

        Parameters
        ----------
        file_queue : multiprocessing.Queue
            The file queue.
        
        matches : multiprocessing.Manager.list
            A list where molecules matches to the pharmacophore will be stored
        
        n_molecules : multiprocessing.Value
            A counter for the total number of molecules screened
            
        pharmacophore : 
            The pharmacophore
        
    """
    while not file_queue.empty():
        file = file_queue.get()
        with open(file, "r") as fp:
            fp.readline()
            for line in fp:
                splitted_line = line.split()
                smiles = splitted_line[0]
                zinc_id = splitted_line[1]
                molecule = Chem.MolFromSmiles(smiles)
                molecule.SetProp("_Name", zinc_id)
                with n_molecules.get_lock():
                    n_molecules.value += 1  
                align_molecule(molecule, matches, pharmacophore)

def get_pharmacophore():
    
    sb_pharmacophore = oph.StructuredBasedPharmacophore().from_pdb("1M7O",ligand_id="3PG:A:5401")
    sb_pharmacophore.remove_elements([0, 1, 3, 4])
    print(f"\nPharmacophore of 1M7O:")
    print(sb_pharmacophore)

    rdkit_pharmacophore = get_rdkit_pharmacophore(sb_pharmacophore)
    
    return sb_pharmacophore, rdkit_pharmacophore

def virtual_screening(dataset_path, pharmacophore, sort=False):
    
    file_queue = get_files(dataset_path)
    print("Started Virtual Screening")
    
    with Manager() as manager:
        
        matches = manager.list()
        n_molecules = Value("i", 0)
        
        pool = Pool(None, screen_files, (file_queue, matches, n_molecules, pharmacophore))
        pool.close()
        pool.join()
        
        # print(matches)
        # print(n_molecules.value)
        if not sort:
            return list(matches), n_molecules.value

        else:
            return list(matches).sort(key=lambda x: x.score), n_molecules.value

def main():
    dataset_path = "/home/daniel/Documents/MyNotebooks/zinc/data/shards"
    _, rdkit_pharmacophore = get_pharmacophore()
    
    matches, n_molecules = virtual_screening(dataset_path, rdkit_pharmacophore, sort=True)
    
    print(f"Number of molecules screened: {n_molecules}")
    print(f"Number of matches: {len(matches)}")
    print(f"Number of fails: {n_molecules - len(matches)}")
    

if __name__=="__main__":
   main()