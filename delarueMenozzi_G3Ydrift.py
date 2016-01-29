'''
Created on Jan 27, 2016

@author: weiluo
'''
from importlib import reload
import delarueMenozzi_simplifedCase_base
reload(delarueMenozzi_simplifedCase_base)

from delarueMenozzi_simplifedCase_base import DelarueMenozziSimplifiedCaseBase
from run_dm_iteration_helpers import dm_iterate_helper

class DelarueMenozzi_G3Ydrift(DelarueMenozziSimplifiedCaseBase):
    '''
    dX_t = -Y_t dt + \sigma dW_t
    dY_t = (Y)^3 dt + Z_t dW_t
    X_0 = x_0, Y_T = X_T
    
    We want to compute the distribution of
    g(Y_t) from 0 to T.
    g = y
    '''

    def __init__(self, A = 1, kappa = 1, *args, **kwargs):
        self.A = A
        self.kappa = kappa
        super().__init__(*args, **kwargs)
    
    def F(self, x, y):
        return -1 * y
    def G(self, time_index, y):
        return y ** 3
    def f(self, x):
        return x
    def g(self, y):
        return y 

class DelarueMenozzi_G3Ydrift_useExpectationOnYdrift(DelarueMenozzi_G3Ydrift):
    '''
    dX_t = -Y_t dt + \sigma dW_t
    dY_t = (eta)^3 dt + Z_t dW_t
    X_0 = x_0, Y_T = X_T
    
    eta_t comes from the previoous iteration
    
    We want to compute the distribution of
    g(Y_t) from 0 to T as eta.
    g = y
    '''


    def __init__(self, eta, *args, **kwargs):
        self.eta = list(eta) 
        super().__init__(*args, **kwargs)
        
    def G(self, time_index, y):
        return self.eta[time_index] ** 3
    
    
def G3_factory(phase, *args, **kwargs):
    if phase == 'init':
        return DelarueMenozzi_G3Ydrift(*args, **kwargs)
    elif phase == 'use_expectation':
        return DelarueMenozzi_G3Ydrift_useExpectationOnYdrift(*args, **kwargs)
    else:
        raise Exception("phase should be " +
                         "either 'init' for the starting phase " +
                         "or 'use_expectation' for the following phase")
def iterate_G3Ydrift(iter_number = 20, *args, **kwargs):
    return dm_iterate_helper(G3_factory, iter_number, *args, **kwargs)

    