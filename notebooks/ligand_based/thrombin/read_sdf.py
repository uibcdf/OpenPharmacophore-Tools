from rdkit import Chem


def read_sdf(file_path):
    """ Reads an sdf file that can contain multiple conformers
        for a molecule.
        
        Parameters
        ----------
        file_path : str
        
        Returns
        -------
        list : [rdkit.Chem.Mol]
    """
    supp = Chem.SDMolSupplier(file_path, removeHs=False)
    molecules = {}
    
    for mol in supp:
        name = mol.GetProp("_Name")
        try:
            molecules[name].AddConformer(mol.GetConformer(), assignId=True)
        except KeyError:
            molecules[name] = mol
    
    return list(molecules.values())
