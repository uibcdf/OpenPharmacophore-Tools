import yaml
import os
import requests


def fetch(pdb_id):
    """ Fetch a pdb file from the Protein Data Bank.

        Parameters
        ----------
        pdb_id : str
            The code of the pdb.
    """
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content.decode()
    else:
        print(f"Failed to fetch {pdb_id}\n"
              f"Status Code {response.status_code}\n"
              f"{url}")
        return ""


def fetch_single_pdb(pdb_code, pdb_dir):
    """ Fetch and write a single pdb file to disk.

        Parameters
        ----------
        pdb_code : str
           The id of the pdb.

        pdb_dir : str
            Path were the files will be saved to.
    """
    pdb_str = fetch(pdb_code)
    # Create a folder for each pdb
    pdb_file_path = os.path.join(pdb_dir, pdb_code)
    if not os.path.isdir(pdb_file_path):
        os.mkdir(pdb_file_path)
    with open(os.path.join(pdb_file_path, pdb_code + ".pdb"), "w") as fp:
        fp.write(pdb_str)
    print(f"Fetched {pdb_code}")


def fetch_pdbs(pdb_codes_file, pdb_dir):
    """ Fetch and write pdb files to disk.

        Parameters
        ----------
        pdb_codes_file : str
            File containing a list of pdb ids.

        pdb_dir : str
            Path were the files will be saved to.
    """
    with open(pdb_codes_file) as fp:
        pdb_ids = fp.readlines()

    for pdb_id in pdb_ids:
        pdb_id = pdb_id.rstrip()
        fetch_single_pdb(pdb_id, pdb_dir)


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


def fetch_all_datasets():
    """ Downloads all the pdbs necessary for each dataset.

        It downloads all the required pdb files, organizes into appropriate
        folders and writes a readme for each dataset.
    """
    download_path = "./test_cases"
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

    print("Finished Downloading PDBs")

