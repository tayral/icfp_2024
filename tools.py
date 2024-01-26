## common tools for exercises
import numpy as np

gate_dic = {
    "H": np.array([[1, 1], [1, -1]])/np.sqrt(2),
    "CNOT": np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1],
                      [0, 0, 1, 0]
                     ]),
    "RX": lambda theta : np.cos(theta/2) * np.identity(2) - 1j * np.sin(theta/2)*np.array([[0, 1], [1, 0]], np.complex128),
    "RY": lambda theta : np.cos(theta/2) * np.identity(2) - 1j * np.sin(theta/2)*np.array([[0, -1j], [1j, 0]], np.complex128),
    "RZ": lambda theta : np.cos(theta/2) * np.identity(2) - 1j * np.sin(theta/2)*np.array([[1, 0], [0, -1]], np.complex128)

}

class Circuit:
    def __init__(self, nqbits, gates):
        self.nqbits = nqbits
        self.gates = gates
        
    def add(self, gate_tuple):
        self.gates.append(gate_tuple)
        
    def __str__(self):
        string = ""
        for gt in self.gates:
            string += str(gt) + "\n"
        return string

def random_circuit(nqbits, nlayers):
    """ create a simple random circuits on nqbits qbits with nlayers layers"""
    circ = Circuit(nqbits, [])
    for indl in range(nlayers):
        for qb in range(nqbits):
            rot = "R" + np.random.choice(["X", "Y", "Z"])
            angle = np.random.random()*2*np.pi
            circ.add((rot, [qb], angle))
        for qb in range(nqbits-1 - indl%2):
            circ.add(("CNOT", [qb+indl%2, qb+1+indl%2]))
    return circ
