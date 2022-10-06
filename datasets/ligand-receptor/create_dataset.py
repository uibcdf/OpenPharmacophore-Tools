from get_ligand_smiles import process_smi_file, write_pdb_ligands_to_smi
from get_pdbs import fetch_all_datasets


def main():

    process_smi_file("./data/Components-smiles-stereo-oe.smi")
    fetch_all_datasets()
    write_pdb_ligands_to_smi()


if __name__ == "__main__":
    main()
