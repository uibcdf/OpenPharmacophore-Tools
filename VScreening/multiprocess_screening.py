from openpharmacophore import StructuredBasedPharmacophore
from openpharmacophore.screening.screening import MultiProcessVirtualScreening


def main():

    dataset_path = "./data/zinc/shards"
    sb_pharmacophore = StructuredBasedPharmacophore().from_pdb("1M7O",ligand_id="3PG:A:5401")
    sb_pharmacophore.remove_elements([0, 1, 3, 4])
    print(f"\nPharmacophore of 1M7O:")
    print(sb_pharmacophore.elements, "\n")
    
    screener = MultiProcessVirtualScreening(sb_pharmacophore)
    screener.screen_db_from_dir(dataset_path, sort=False)
    
    screener.print_report()
    
    print("5 first matches:\n")
    print(screener.matches[0:5])


if __name__=="__main__":
    main()