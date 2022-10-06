import mdtraj as mdt
import os


def process_smi_file(file_name):
    """ Process Components-smiles-stereo-oe.smi file removing compound names.

        This will create a file that maps pdb ids of ligands to its corresponding smiles.
    """
    smiles = []
    with open(file_name) as fp:
        for line in fp.readlines():
            components = line.split()
            if len(components) > 2:
                smiles.append(components[0:2])

    smiles.sort(key=lambda x: x[1])
    with open("./data/smiles-stereo-mod.txt", "w") as fp:
        for smi in smiles:
            if len(smi[1]) <= 3:
                line = smi[1] + " " + smi[0] + '\n'
                fp.write(line)


def load_smiles_db():
    """ Returns a dictionary that maps pdb ids to smiles.

        Returns
        -------
        pdb_to_smiles : dict[str, str]
    """
    pdb_to_smiles = {}
    with open("./data/smiles-stereo-mod.txt") as fp:
        for line in fp.readlines():
            pdb_id, smiles = line.split()
            pdb_to_smiles[pdb_id] = smiles
    return pdb_to_smiles


non_ligand_residues = [
    "ALA", "ARG", "ASN", "ASP", "ASX",
    "CYS", "GLU", "GLN", "GLX", "GLY",
    "HIS", "ILE", "LEU", "LYS", "MET",
    "PHE", "PRO", "SER", "THR", "TRP",
    "TYR", "VAL", "HOH", "DOD",
]


def find_ligands_in_traj(topology_file):
    """ Returns a list of ligand ids in a trajectory.

        Parameters
        ----------
        topology_file : str
            A topology file such as a pdb.

        Returns
        -------
        ligands : list[str]
            A list of the ligands ids in the topology file
    """
    topology: mdt.Topology

    traj = mdt.load(topology_file)
    topology = traj.topology
    n_residues = topology.n_residues

    # Find all possible ligand residues
    ligands = []
    for ii in range(n_residues):
        residue = topology.residue(ii)
        if residue.name not in non_ligand_residues \
                and residue.n_atoms > 5 \
                and residue.name not in ligands:
            ligands.append(residue.name)

    return ligands


def create_ligands_smi_file(ligand_ids, pdb_path, id_to_smiles, failures):
    """ Creates a smi file from a list of PDB ligand ids.

        Parameters
        ----------
        ligand_ids : list[str]
        pdb_path : str
        id_to_smiles : dict[str, str]
        failures : list[str]
    """
    lines = ""
    for ligand in ligand_ids:
        try:
            smiles = id_to_smiles[ligand]
            lines += smiles + " " + ligand + "\n"
        except KeyError:
            failures.append(ligand)
            continue

    with open(os.path.join(pdb_path, "ligands.smi"), "w") as fp:
        fp.write(lines)


def write_pdb_ligands_to_smi():
    """ Obtain the smiles of each ligand in each pdb and save it to a file.
    """
    pdb_to_smiles = load_smiles_db()
    num_files = 0
    ligand_fails = []
    pdb_fails = []
    num_ligand_fails = 0

    for root, directories, filenames in os.walk("./data/test_cases"):
        for file in filenames:
            if file.endswith(".pdb"):
                num_files += 1
                pdb_id = file.split(".")[0]
                ligand_ids = find_ligands_in_traj(os.path.join(root, file))
                create_ligands_smi_file(ligand_ids, root, pdb_to_smiles, ligand_fails)

                if len(ligand_fails) > num_ligand_fails:
                    num_ligand_fails = len(ligand_fails)
                    pdb_fails.append(pdb_id)

                print(f"Created file for {pdb_id}")

    print(f"\n\n{num_files} pdb files total")
    print(f"Failed to get smiles for {len(ligand_fails)} ligands")
    print(f"{len(pdb_fails)} pdb files presented problems\n\n")

    if len(ligand_fails) > 0:
        print("A smiles could not be obtained for the following ligand ids:")
        print(ligand_fails)
        print("The pdbs that presented issues were:")
        print(pdb_fails)
