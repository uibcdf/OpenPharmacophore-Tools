# Ligand preparation

PDBID: 1QKU

## Tasks

- Extract a ligand from the 1QKU pdb and write a new pdb file with it.
- Load the PDB with rdkit
- Is the molecule correct? are the bonds order correct or you have only single bonds...
- Make a template molecule from the smile: 'C[C@]12CC[C@@H]3c4ccc(cc4CC[C@H]3[C@@H]1CC[C@@H]2O)O'
- Assign bond orders to your original molecule (pdb) from the template. 
- Add hydrogens to the ligand.
- Build a first ligand system parameterized with the last version of the classic amber forcefield for
  ligands: GAFF.
- Solvate it with tip3p waters (truncated octahedral box with a 14 angstroms clearance).
- Build a second ligand system with the recent version 1.0 of the OpenForcefield Parsley.
- Solvate it with tip3p waters (truncated octahedral box with a 14 angstroms clearance).

### Useful tools

- Python, Jupyter, etc.
- OpenMM
- OpenForcefield
- RDKit

### Useful sources

http://docs.openmm.org/latest/userguide/index.html    
http://docs.openmm.org/latest/api-python/     
https://github.com/openmm/openmm-cookbook     
https://www.youtube.com/watch?v=0S9Pj33IVk0&t=1s
https://openforcefield.org/
https://www.youtube.com/channel/UCh0aJSUm_sYr7nuTzhW806g/videos
https://github.com/openforcefield/openff-toolkit
https://open-forcefield-toolkit.readthedocs.io/en/latest/index.html
https://github.com/tdudgeon/simple-simulate-complex/blob/master/simulateComplexWithSolvent.py
https://github.com/openmm/openmmforcefields
https://open-forcefield-toolkit.readthedocs.io/en/latest/examples.html


