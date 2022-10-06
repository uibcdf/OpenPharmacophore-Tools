

def process_smi_file(file_name):
    """ Process Components-smiles-stereo-oe.smi file removing compound names.

        This will create a file that maps pdb ids of ligands to its corresponding smiles.
    """
    smiles = []
    with open(file_name) as fp:
        for line in fp.readlines():
            components = line.split()
            if len(components) > 2:
                smiles.append(components[0:2])

    smiles.sort(key=lambda x: x[1])
    with open("./data/smiles-stereo-mod.txt", "w") as fp:
        for smi in smiles:
            if len(smi[1]) <= 3:
                line = smi[1] + " " + smi[0] + '\n'
                fp.write(line)


if __name__ == "__main__":
    process_smi_file("./data/Components-smiles-stereo-oe.smi")
    print("DONE")
