import mdtraj as mdt
import openpharmacophore.pharmacophore.pl_interactions as pli
import os


def save_ligand_to_pdb(traj, chain, lig_id, path):
    """ Extract chains from a trajectory

        Parameters
        ----------
        traj: mdtraj.Trajectory

        chain: int

        lig_id : str

        path: str

    """
    ligand = traj.atom_slice(
        [atom.index for atom in traj.topology.atoms if (atom.residue.chain.index == chain)]
    )
    file_name = "_".join(lig_id.split(":")) + "_chain.pdb"
    ligand.save_pdb(os.path.join(path, file_name))


def extract_ligands():
    """Extract the lignads in each pdb and save them to pdb files.
    """
    for root, directories, filenames in os.walk("./test_cases"):
        for file in filenames:
            if file.endswith(".pdb"):
                traj = mdt.load(os.path.join(root, file))
                ligands = pli.find_ligands_in_traj(traj)
                for lig in ligands:
                    chain = pli.chain_names.index(lig.split(":")[-1])
                    save_ligand_to_pdb(traj, chain, lig, root)
                    print(f"Created file for {lig}")
