from compute import generate_instance, plot_vals_1, plot_vals_2, plot_vals_3
import numpy as np
from matplotlib import pyplot as plt
from shapleyeff import calculate_SV_eff
import time
from shapleyeff import calculate_SV_eff
from coalition import calculate_shapley_value

c = 5
# gammas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
# num_builders = [5, 5, 5, 15, 15, 15, 30, 30, 30]
# num_ofas =     [1, 2, 3, 1, 2, 3, 1, 2, 3]
# num_builders = [2, 3, 4]
# num_ofas = [1, 1, 1]
# distributions = ['Triangular', 'Uniform', 'Normal']
# values = None

# # Plot 1 
# # to generate plot one uncomment violin_plot from generate_isntance
# for num_b, num_o in zip(num_builders, num_ofas):
#     for dist in distributions:
#         print(c)
#         [(a,b), (d, e), (f, g)],[(mean_ofa, std_ofa), (mean_builder, std_builder), (mean_proposer, std_proposer)] = generate_instance(c, gammas, num_b, num_o, dist)
#         # # computing coefficient of variation of each player
#         cv_ofa = std_ofa[0][0] / mean_ofa[0][0] if mean_ofa[0][0] != 0 else 0
#         cv_builder = std_builder[0][0] / mean_builder[0][0] if mean_builder[0][0] != 0 else 0
#         cv_proposer = std_proposer[0] / mean_proposer[0] if mean_proposer[0] != 0 else 0
#         print(f"Distribution: {dist}, Num Builders: {num_b}, Num OFAs: {num_o}")
#         print(f"OFAs: CV = {cv_ofa:.4f}")
#         print(f"Builders: CV = {cv_builder:.4f}")
#         print(f"Proposers: CV = {cv_proposer:.4f}")

# # Plot 2
# fixed_builders = 4
# fixed_ofas = 1
# type = 'Triangular'
# gammas = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
# valsA, valsC = generate_instance(c, gammas, fixed_builders, fixed_ofas, type)
# plot_vals_2(gammas, fixed_builders, fixed_ofas, type, valsA, valsC)

# Plot 3
num_builders = [2, 3, 4, 5, 6, 7, 8, 9, 10]
num_ofas = [4, 4, 4, 4, 4, 4, 4, 4, 4]
distributions = ['Triangular']
fixed_gammas = [1.27]
list_valuesA, list_valuesC = [], [] # entire list of values
for i in range(len(num_builders)): # for each builder
    lvA, lvC = [], [] # list of values for each builder
    for dist in distributions: # for each distribution
        valuesA, valuesC = generate_instance(c, fixed_gammas, num_builders[i], num_ofas[i], dist)
        # generates mean utilities
        lvA.append(valuesA)
        lvC.append(valuesC)
    list_valuesA.append(lvA) # list_valuesA = (num_builders, len(distributions), 3, 2, len(gammas), num_players)
    list_valuesC.append(lvC) # list_valuesC = 
# print(len(list_valuesA), len(list_valuesA[0]), len(list_valuesA[0][1]), len(list_valuesA[0][0][0]))
plot_vals_3(fixed_gammas, num_builders, num_ofas[0], distributions, list_valuesA, list_valuesC)