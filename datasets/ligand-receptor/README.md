#  Protein-ligand complexes datasets

This directory contains datasets, taken from the literature, of protein-ligand complexes
that can be used for structured based pharmacophore-elucidation.

The following datasets are included:

- CommonHitsApproach
- ERalpha
- KinaseInhibitors
- InsulinGF
- Rhinovirus
- Tyrosine Kinase
- Cruft
- Plip

Each one consists of a set of pdb files, a smi file containing the smiles of the ligands present
in each protein-ligand complex as well as a pdb file for each ligand.

Because there are a lot pdb files, they are not stored in this repository. However, the datasets can
be downloaded automatically running the script create_dataset.py:

```bash

python create_dataset.py
```
