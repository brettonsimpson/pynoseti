import numpy as np

def compile_image(quabo_1, quabo_2, quabo_3, quabo_4):

    quabo_2 = np.rot90(quabo_2, -1)
    #

    quabo_3 = np.rot90(quabo_3, -2)
    #

    quabo_4 = np.rot90(quabo_4, -3)
    #

    final_quadrant_1 = np.kron(np.array([[0,1],[0,0]]), quabo_3)
    #

    final_quadrant_2 = np.kron(np.array([[0,0],[0,1]]), quabo_4)
    #

    final_quadrant_3 = np.kron(np.array([[0,0],[1,0]]), quabo_1)
    #

    final_quadrant_4 = np.kron(np.array([[1,0],[0,0]]), quabo_2)
    #

    return final_quadrant_1+final_quadrant_2+final_quadrant_3+final_quadrant_4