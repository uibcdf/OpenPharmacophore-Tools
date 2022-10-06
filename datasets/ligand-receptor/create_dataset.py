from fetch_pdbs import fetch_single_pdb, fetch_pdbs
import yaml
import os


def load_datasets_info():
    """ Loads datasets.yaml into a dictionary"""
    with open("./data/datasets.yaml") as fp:
        db = yaml.load(fp, Loader=yaml.FullLoader)
    return db


def write_readme(dataset_path, dataset_name, comments, reference):
    """ Writes a readme file for the dataset."""
    content = "# " + dataset_name + '\n'
    if comments is not None:
        content += comments + '\n'
    content += "#### References\n"
    content += reference
    file_path = os.path.join(dataset_path, dataset_name.lower() + ".md")
    with open(file_path, "w") as fp:
        fp.write(content)


def main():
    """ Creates the datasets.

        It downloads all the required pdb files, organizes into appropriate
        folders and writes a readme for each dataset.
    """
    download_path = "./data/test_cases"
    pdb_codes_path = "./data/pdb_codes"

    if not os.path.isdir(download_path):
        os.mkdir(download_path)

    datasets = load_datasets_info()
    for dataset_name, info in datasets.items():
        name = dataset_name.lower()
        print(f"\n\nCREATING DATASET {name.upper()}")
        dataset_path = os.path.join(download_path, name)
        if not os.path.isdir(dataset_path):
            os.mkdir(dataset_path)
        if "PDB codes file" in info:
            fetch_pdbs(os.path.join(pdb_codes_path, info["PDB codes file"]),
                       dataset_path)
        elif "PDB code" in info:
            fetch_single_pdb(info["PDB code"], dataset_path)
        write_readme(dataset_path, name.capitalize(),
                     info["Comments"], info["Reference"])

    print("DONE")


if __name__ == "__main__":
    main()
