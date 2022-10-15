from get_ligand_smiles import load_smiles_db
from rdkit.Chem import AllChem
import os
from pprint import pprint


class NumberOfAtomsError(ValueError):

    def __init__(self, ligand_id, smiles):

        message = (
            f"Ligand {ligand_id} does not contain the same number of "
            f"atoms as the template smiles {smiles}.\n"
        )
        super().__init__(message)


class SmilesToMolError(ValueError):

    def __init__(self, ligand_id, smiles):

        message = (
            f"Ligand {ligand_id} with smiles {smiles} could not be converted "
            f"to molecule.\n"
        )
        super().__init__(message)


class LoadMoleculeError(ValueError):

    def __init__(self, name, file):

        message = f"Molecule {name} from file {file} could not be loaded "
        super().__init__(message)


def fix_bond_orders_from_smiles(molecule, smiles, ligand_id):

    template = AllChem.MolFromSmiles(smiles)

    if template is None:
        raise SmilesToMolError(ligand_id, smiles)

    if template.GetNumAtoms() != molecule.GetNumAtoms():
        raise NumberOfAtomsError(ligand_id, smiles)

    return AllChem.AssignBondOrdersFromTemplate(template, molecule)


def fix_bond_orders(print_ligands=False):
    """ Fix the bond orders of the ligands contained in the dataset.

        To do this we'll use their smiles and a template molecule
    """
    pdb_to_smiles = load_smiles_db()

    fails_num_atoms = []
    fails_other = []
    fails_ligand_names = set()
    fails_smiles = 0
    fails_load_pdb = 0

    success_ligand_names = set()
    n_success = 0
    total = 0

    for root, directories, filenames in os.walk("./test_cases"):
        for file in filenames:
            total += 1
            if file.endswith(".pdb"):
                ligand_id = file.split("_")
                if len(ligand_id) > 1:
                    ligand_name = ligand_id[0]
                    if ligand_name == "A":
                        ligand_name = "ADE"

                    try:
                        smiles = pdb_to_smiles[ligand_name]
                    except KeyError:
                        print(f"Smiles not found for {ligand_name}")
                        continue

                    molecule = AllChem.MolFromPDBFile(os.path.join(root, file))
                    if molecule is None:
                        fails_other.append(os.path.join(root, file))
                        fails_ligand_names.add(ligand_name)
                        fails_load_pdb += 1
                        continue

                    try:
                        fix_bond_orders_from_smiles(molecule, smiles, ligand_id)
                    except NumberOfAtomsError:
                        fails_num_atoms.append(os.path.join(root, file))
                        fails_ligand_names.add(ligand_name)
                    except (SmilesToMolError, ValueError):
                        fails_other.append(os.path.join(root, file))
                        fails_ligand_names.add(ligand_name)
                        fails_smiles += 1
                        
                    n_success += 1
                    success_ligand_names.add(ligand_name)
                    print(f"Fixed molecule for {ligand_name}")

    total_fails = fails_num_atoms + fails_other
    if print_ligands:
        pprint(total_fails)
        pprint(fails_ligand_names)
        pprint(success_ligand_names)

    percentage_success = len(success_ligand_names) / (len(success_ligand_names) + len(fails_ligand_names))
    percentage_success *= 100
    print(f"\n\nTotal files {total}")
    print(f"Total different ligands: {len(success_ligand_names) + len(fails_ligand_names)}")
    print(f"Number of files successfully fixed: {n_success}")
    print(f"Number of different ligands fixed: {len(success_ligand_names)}")
    print(f"Number of files failed to be fixed: {len(total_fails)}")
    print(f"Number of different ligands that could not be fixed: {len(fails_ligand_names)}")
    print(f"Pdb files containing incorrect number of atoms: {len(fails_num_atoms)}")
    print(f"Pdb files that could not be loaded: {fails_load_pdb}")
    print(f"Ligand whose smile could not be loaded {fails_smiles}")
    print(f"Percentage success: {percentage_success:.2f}%")
    print("\nDONE")


if __name__ == "__main__":
    fix_bond_orders(False)
