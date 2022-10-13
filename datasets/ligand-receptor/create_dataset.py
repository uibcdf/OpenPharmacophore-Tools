from get_ligand_smiles import process_smi_file, write_pdb_ligands_to_smi
from get_pdbs import fetch_all_datasets
from extract_ligands_to_pdb import extract_ligands


def main():

    process_smi_file("./data/Components-smiles-stereo-oe.smi")
    fetch_all_datasets()
    write_pdb_ligands_to_smi()
    extract_ligands()
    print("DONE")


if __name__ == "__main__":
    main()
