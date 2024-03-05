## Exercise 1
import numpy as np
from tools import Circuit, gate_dic

class State:
    def __init__(self, nqbits):
        self.nqbits = nqbits
        self.shape = (2,)*nqbits
        self.state = np.zeros(self.shape, np.complex128)
        self.state[(0,)*nqbits] = 1
        
    def apply(self, gate_matrix, qbits):
        """
        Args:
            gate (np.array): gate matrix
            qbits (list<int>): qubits on which the gate acts
        """
        self.state = np.moveaxis(self.state, qbits, np.arange(len(qbits)))
        self.state = np.reshape(self.state, (2**len(qbits), 2**(self.nqbits - len(qbits))))
        self.state = gate_matrix.dot(self.state)
        self.state = np.reshape(self.state, self.shape)
        self.state = np.moveaxis(self.state, np.arange(len(qbits)), qbits)
        
    def __str__(self):
        state = self.to_vec()
        
        string = ""
        for ind in range(2**self.nqbits):
            string += "|"+format(ind, '0'+str(self.nqbits)+'b')+">" +" : "+str(state[ind])+" \n"
        return string
        
    def to_vec(self):
        return np.reshape(self.state, 2**self.nqbits)
    
class StateVectorQPU:
    """
    Args:
        nqbits (int): number of qubits
        gate_dic (dic{string, matrix or lambda(matrix)): keys: gate names, values: matrices
    """
    def __init__(self, nqbits, gate_dic):
        self.state = State(nqbits)
        self.gate_dic = gate_dic
    def submit(self, circuit):
        assert(circuit.nqbits == self.state.nqbits)
        for gate_tuple in circuit.gates:
            matrix = self.gate_dic[gate_tuple[0]] if len(gate_tuple)==2\
                        else self.gate_dic[gate_tuple[0]](gate_tuple[2])
            self.state.apply(matrix, gate_tuple[1])
            
        return self.state
