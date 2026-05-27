import numpy as np
import time as time
from shapleyeff import calculate_SV_eff

c = 5
g = 1.27
dist = 'Triangular'
num_builders = 30
num_ofas = 3
num_iters = 10000
v_pbs = np.zeros((num_iters, num_builders))
v_ofa = np.zeros((num_iters, num_ofas, num_builders))
for i in range(num_iters): # for a particular instance
    v_o = np.random.triangular(left=0, mode=g*c/2, right=g*c,size=(num_ofas,num_builders))
    # generate backrunning valuations of dimensions num_ofas x num_builders
    # from triangular distribution
    v_p = np.random.triangular(left=0,mode=c/2, right = c, size=num_builders)
    # generate arbitrage valuations of dimensions num_builders
    # from triangular distribution
    v_pbs[i, :] = v_p
    v_ofa[i, :, :] = v_o
print("data generation done")
start = time.time()
for i in range(num_iters):
    a = v_pbs[i]
    o = v_ofa[i]
    calculate_SV_eff(num_builders, num_ofas, a, o)
end = time.time()
print("Time taken for num_builders = {}, num_ofas = {}, iteration {}: {}".format(num_builders, num_ofas, iter, 1000.0 * (end - start)/num_iters))