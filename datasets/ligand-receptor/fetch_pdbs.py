import os
import requests
import sys


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


if __name__ == "__main__":
    if len(sys.argv) == 3:
        pdb_codes = sys.argv[1]
        download_path = sys.argv[2]
        fetch_pdbs(pdb_codes, download_path)
    else:
        raise ValueError("Expected the following arguments: pdb_codes, download_path")
