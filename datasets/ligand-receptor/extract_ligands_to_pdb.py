import mdtraj as mdt
import openpharmacophore.pharmacophore.pl_interactions as pli
import os


def save_ligand_to_pdb(traj, lig_id, chain_index, path):
    """ Extract chains from a trajectory

        Parameters
        ----------
        traj: mdtraj.Trajectory
        chain_index : int
        lig_id : str
        path: str

    """
    ligand_name, _ = lig_id.split(":")
    ligand = traj.atom_slice(
        [atom.index for atom in traj.topology.atoms if
         (atom.residue.name == ligand_name and atom.residue.chain.index == chain_index)]
    )
    assert ligand.n_atoms > 0, f"{lig_id} failed to extract"
    file_name = "_".join(lig_id.split(":")) + "_chain.pdb"
    ligand.save_pdb(os.path.join(path, file_name))


def extract_ligands():
    """Extract the ligands in each pdb and save them to pdb files.
    """
    for root, directories, filenames in os.walk("./test_cases"):
        for file in filenames:
            if file.endswith(".pdb"):
                traj = mdt.load(os.path.join(root, file))
                ligands = pli.find_ligands_in_traj(traj)
                for lig in ligands:
                    chain = lig.split(":")[-1]
                    chain_index = pli.chain_names.index(chain)
                    save_ligand_to_pdb(traj, lig, chain_index, root)
                    print(f"Created file for {lig}")
