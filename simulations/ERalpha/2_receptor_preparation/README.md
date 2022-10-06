# Receptor simulation

PDBID: 1QKU

## Tasks

- Extract a receptor from the 1QKU pdb and write a new pdb file with it.
- Check if the receptor has missing atoms, residues or terminals. Check if all aminoacids are
  common aminoacids.
- Add hydrogens to the molecule. Do you see residues that could be with a differen protonation
  state? What happens with them when you change the pH of the environment to protonate the system?
- Get the charge (coulombic) of the protein. Is neutral? What are the charged residues?
- Solvate the system with TIP3P water molecules in a truncated octahedral box with the protein in
  the center and the limits of the box 14 angstroms away from the protein surface (at least).
- Did you add ions to the box?
- Explore the openmm object: Topology

### Useful tools

- Python, Jupyter, etc.
- PDBFixer
- OpenMM
- Modeller (in OpenMM)

### Useful sources

http://docs.openmm.org/latest/userguide/index.html    
http://docs.openmm.org/latest/api-python/     
https://github.com/openmm/openmm-cookbook     
https://github.com/openmm/pdbfixer     
https://htmlpreview.github.io/?https://github.com/openmm/pdbfixer/blob/master/Manual.html     


