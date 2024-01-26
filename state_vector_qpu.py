## Exercise 1
import numpy as np
from tools import Circuit, gate_dic

class State:
    def __init__(self, nqbits):
        self.nqbits = nqbits
        self.shape = (2,)*nqbits
        self.state = np.zeros(self.shape, np.complex128)
        self.state[(0,)*nqbits] = 1
        
    def apply(self, gate, qbits, param=None):
        self.state = np.moveaxis(self.state, qbits, np.arange(len(qbits)))
        self.state = np.reshape(self.state, (2**len(qbits), 2**(self.nqbits - len(qbits))))
        matrix = gate_dic[gate] if param is None else gate_dic[gate](param)
        self.state = matrix.dot(self.state)
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
    def __init__(self, nqbits):
        self.state = State(nqbits)
        
    def submit(self, circuit):
        assert(circuit.nqbits == self.state.nqbits)
        for gate_tuple in circuit.gates:
            self.state.apply(*gate_tuple)
            
        return self.state
