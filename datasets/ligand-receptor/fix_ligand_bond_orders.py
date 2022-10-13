from get_ligand_smiles import load_smiles_db
import openpharmacophore.pharmacophore.pl_interactions as pli
from rdkit import Chem
import os
from pprint import pprint


def fix_bond_orders():
    pdb_to_smiles = load_smiles_db()

    fails = []
    for root, directories, filenames in os.walk("./test_cases"):
        for file in filenames:
            if file.endswith(".pdb"):
                ligand_id = file.split("_")
                if len(ligand_id) > 1:
                    ligand_name = ligand_id[0]
                    try:
                        smiles = pdb_to_smiles[ligand_name]
                    except KeyError:
                        print(f"Smiles not found for {ligand_name}")
                        continue
                    molecule = Chem.MolFromPDBFile(os.path.join(root, file))
                    try:
                        pli.fix_bond_order_from_smiles(molecule, smiles)
                    except:
                        fails.append(os.path.join(root, file))
                    print(f"Fixed molecule for {ligand_name}")

    print(f"\nNumber of failures {len(fails)}")
    print(f"Following ligands could not be fixed")
    pprint(fails)
    print("DONE")


if __name__ == "__main__":
    fix_bond_orders()
