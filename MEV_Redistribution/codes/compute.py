from matplotlib import pyplot as plt
import numpy as np;
from auction import calculate_vcg
from coalition import calculate_shapley_value
from shapleyeff import calculate_SV_eff
import pandas as pd
import seaborn as sns

# plt.rcParams['text.usetex'] = True

def meanstd(proposer, builder, ofa):
    mean_ofa = np.around(np.mean(ofa, axis=1), decimals=3)
    std_ofa = np.around(np.std(ofa, axis=1), decimals=3)

    mean_builder = np.around(np.mean(builder, axis=1), decimals=3)
    std_builder = np.around(np.std(builder, axis=1), decimals=3)

    mean_proposer = np.around(np.mean(proposer, axis=1), decimals=3)
    std_proposer = np.around(np.std(proposer, axis=1), decimals=3)

    return [(mean_ofa, std_ofa), (mean_builder, std_builder), (mean_proposer, std_proposer)]

def generate_instance(c, gammas, num_builders, num_ofas, type):
    num_iters = 10000
    builderA = np.zeros((len(gammas),num_iters,num_builders)) # each gamma, 10000 instances, num_builders
    ofaA = np.zeros((len(gammas),num_iters,num_ofas)) # each gamma, 10000 instances, num_ofas
    proposerA = np.zeros((len(gammas), num_iters)) # each gamma, 10000 instances

    builderC = np.zeros((len(gammas),num_iters,num_builders)) # each gamma, 10000 instances, num_builders
    ofaC = np.zeros((len(gammas),num_iters,num_ofas)) # each gamma, 10000 instances, num_ofas
    proposerC = np.zeros((len(gammas), num_iters)) # each gamma, 10000 instances

    for g in range(len(gammas)): # for a particular gamma
        for i in range(num_iters): # for a particular instance
            if i % 2000 == 0:
                print(i)
            if type == 'Triangular': # if distribution is triangular
                v_ofa = np.random.triangular(left=0, mode=gammas[g]*c/2, right=gammas[g]*c,size=(num_ofas,num_builders))
                # generate backrunning valuations of dimensions num_ofas x num_builders
                # from triangular distribution
                v_pbs = np.random.triangular(left=0,mode=c/2, right = c, size=num_builders)
                # generate arbitrage valuations of dimensions num_builders
                # from triangular distribution
            
            elif type == 'Uniform': # if distribution is uniform
                v_ofa = np.random.uniform(0,gammas[g]*c,(num_ofas,num_builders))
                # generate backrunning valuations of dimensions num_ofas x num_builders
                # from uniform distribution
                v_pbs = np.random.uniform(0,c, num_builders)
                # generate arbitrage valuations of dimensions num_builders
                # from uniform distribution
            elif type == 'Exponential': # if distribution is exponential
                v_ofa = np.random.exponential(gammas[g]*c/2,(num_ofas,num_builders))
                # generate backrunning valuations of dimensions num_ofas x num_builders
                # from exponential distribution
                v_pbs = np.random.exponential(c/2, num_builders)
                # generate arbitrage valuations of dimensions num_builders
                # from exponential distribution
            elif type == 'Normal': # if distribution is normal
                v_ofa = np.random.normal(loc=gammas[g]*c/2, scale=gammas[g], size=(num_ofas,num_builders))
                # generate backrunning valuations of dimensions num_ofas x num_builders
                # from normal distribution
                v_pbs = np.random.normal(loc=c/2, scale=1, size=num_builders)
                # generate arbitrage valuations of dimensions num_builders
                # from normal distribution
            h_ofas, h_pbs, utility, payment_pbs, payments_ofa = calculate_vcg(v_ofa,v_pbs)
            # execute auctions
            ofaA[g][i] = payments_ofa # ofa utility in auction with gamma g and instance i
            builderA[g][i] = utility # builder utility in auction with gamma g and instance i
            proposerA[g][i] = payment_pbs # proposer utility in auction with gamma g and instance i

            
            shapley_values = calculate_SV_eff(num_builders, num_ofas, v_pbs, v_ofa)
            # execute MEV-Game
            proposerC[g][i] = shapley_values[0] # proposer utility in MEV-Game with gamma g and instance i
            builderC[g][i] = shapley_values[1:num_builders+1] # builder utility in MEV-Game with gamma g and instance i
            ofaC[g][i] = shapley_values[num_builders+1:] # ofa utility in MEV-Game with gamma g and instance i
         
            # print(shapley_values)
            # return None
            # break

            # print(*v_ofa.reshape(-1,), *utility, *h_ofas+1, h_pbs+1, payment_pbs, *payments_ofa, gamma, sep=',') 
        # break
        # violin_plot(proposerA, proposerC, builderA, builderC, ofaA, ofaC, num_iters, g, num_builders, num_ofas, gammas, type)
    return meanstd(proposerA, builderA, ofaA), meanstd(proposerC, builderC, ofaC)
    # return mean and standard deviation of auction and MEV-Gane for each setup


def plot_vals_1(gammas, num_builders, num_ofas, distributions, valuesA, valuesC):
    x_proposer = [r'P']
    x_builders = [r'B$_' + str(i+1) + '$'  for i in range(num_builders)]
    x_ofas = [r'O$_' + str(i+1) + '$'  for i in range(num_ofas)]

    x_roles = x_proposer + x_builders + x_ofas
    x_positions = np.arange(0, 4*len(x_roles), 4) + 1

    offset = 0.5
    max_vals = None
    min_vals = None
    j = 0
    # for j,vals in enumerate(valuesA):
    for dist in range(len(distributions)):
        for g in range(len(gammas)):
            for valsA, valsC in zip(valuesA, valuesC):
                # each auction instance and coalition instance
                plt.figure(figsize=(10, 6))

                (mean_proposerA, std_proposerA) = valsA[2]
                (mean_builderA, std_builderA) = valsA[1]
                (mean_ofaA, std_ofaA) = valsA[0]

                (mean_proposerC, std_proposerC) = valsC[2]
                (mean_builderC, std_builderC) = valsC[1]
                (mean_ofaC, std_ofaC) = valsC[0]


                meansA = np.concatenate((np.array([mean_proposerA[g]]) , mean_builderA[g], mean_ofaA[g]), axis=0)
                stdsA = np.concatenate((np.array([std_proposerA[g]]), std_builderA[g], std_ofaA[g]), axis=0)
                
                meansC = np.concatenate((np.array([mean_proposerC[g]]) , mean_builderC[g], mean_ofaC[g]), axis=0)
                stdsC = np.concatenate((np.array([std_proposerC[g]]), std_builderC[g], std_ofaC[g]), axis=0)
                # means = means.flatten()
                # stds = stds.flatten()
                max_valsA = np.max(meansA+stdsA)
                min_valsA = np.min(meansA-stdsA)

                max_valsC = np.max(meansC+stdsC)
                min_valsC = np.min(meansC-stdsC)

                min_delta_val = np.min(meansA - meansC)

                plt.bar(x_positions + offset, meansA, yerr = stdsA, align='center', alpha=0.7, ecolor='black', capsize=10,width=0.5, label = r'Auction: $\gamma$ = ' + str(gammas[g]), color=f'C{0}')
                plt.bar(x_positions + offset*2, meansC, yerr = stdsC, align='center', alpha=0.7, ecolor='blue', capsize=10, width=0.5, label = r'Shapley: $\gamma$ = ' + str(gammas[g]), color=f'C{1}')
                # print(meansA - meansC)
                plt.bar(x_positions + offset*3, np.around(meansA-meansC, decimals=3), align='center', alpha=0.7, ecolor='red',  capsize=10, width=0.5, label = r'Delta: $\gamma$ = ' + str(gammas[g]), color=f'C{2}')

                # plt.errorbar(x_positions + offset*j*2, means, yerr = stds, linestyle='None', label = 'Mean for Gamma = ' + str(gammas[2]) + ' and ' + distributions[j] + ' Distribution', color=f'C{j+1}')
                i = 0
                for valA, valC in zip(meansA, meansC):
                    plt.annotate(f'{valA}', (x_positions[i] + offset, valA), textcoords="offset points", xytext=(3,2), ha='center')
                    plt.annotate(f'{valC}', (x_positions[i] + offset*2, valC), textcoords="offset points", xytext=(3,2), ha='center')
                    plt.annotate(f'{np.around(valA-valC,decimals=3)}', (x_positions[i] + offset*3, np.around(valA-valC, decimals=3)), textcoords="offset points", xytext=(3,2), ha='center')
                    i += 1

                # plt.bar(x_positions + offset + (offset)*j*2, stds, width=0.5, label = 'Std Dev for Gamma = ' + str(gammas[2]) + ' and ' + distributions[j] + ' Distribution', color=f'C{j+3}')
                # for i, val in enumerate(stds):
                #     plt.annotate(f'{val}', (x_positions[i] + offset + (offset)*j*2, val), textcoords="offset points", xytext=(3,2), ha='center')

                # plt.title('Means and Standard Deviation of Revenue with ' + str(num_ofas) + ' OFAs and ' + str(num_builders) + ' Builders with ' + distributions[j] + ' Distribution ')
                
                plt.xlim(0, 4*len(x_positions))
                plt.ylim(min(min_valsA, min_valsC, min_delta_val) -0.025, 1.4*max(max_valsA, max_valsC))
                plt.xticks(x_positions + offset*(2) , x_roles)
                plt.xlabel('Roles')
                plt.ylabel('Mean and Standard Deviation')
                plt.legend()
                
                plt.savefig('Means_and_Std_Dev_of_Revenue_in_with_' + str(num_ofas) + '_OFAs_and_' + str(num_builders) + '_Builders_with_' + distributions[j] + '_Distribution_' + '.png', bbox_inches='tight')
                plt.show()
                with open('Means and Std Dev of Revenue in with ' + str(num_ofas) + ' OFAs and ' + str(num_builders) + ' Builders with ' + distributions[j] + ' Distribution ' + '.txt', 'w') as file:
                    file.write('Roles\tMean Auction\tStd Dev Auction\tMean Shapley\tStd Dev Shapley\tDelta\n')
                    for i in range(len(x_roles)):
                        file.write(f"{x_roles[i]}\t{meansA[i]}\t{stdsA[i]}\t{meansC[i]}\t{stdsC[i]}\t{np.around(meansA[i]-meansC[i], decimals=3)}\n")
                j+=1
def plot_vals_2(gammas, num_builders, num_ofas, type, valsA, valsC):
    plt.figure(figsize=(10, 8))
    builder_valsA, builder_valsC = [], []
    ofp_valsA, ofp_valsC = [], []
    (mean_proposerA, std_proposerA) = valsA[2]
    (mean_builderA, std_builderA) = valsA[1]
    (mean_ofaA, std_ofaA) = valsA[0]
    
    plt.xticks(ticks=gammas, labels=gammas)
    for i in range(num_builders):
        builder_valsA.append(mean_builderA[:,i])
    for i in range(num_ofas):
        ofp_valsA.append(mean_ofaA[:,i])
    avg_builderA = np.mean(builder_valsA, axis=0)
    avg_ofpA = np.mean(ofp_valsA, axis=0)
    
    (mean_proposerC, std_proposerC) = valsC[2]
    (mean_builderC, std_builderC) = valsC[1]
    (mean_ofaC, std_ofaC) = valsC[0]
    for i in range(num_builders):
        builder_valsC.append(mean_builderC[:,i])
    for i in range(num_ofas):
        ofp_valsC.append(mean_ofaC[:,i])
    avg_builderC = np.mean(builder_valsC, axis=0)
    avg_ofpC = np.mean(ofp_valsC, axis=0)
    plt.plot(gammas, mean_proposerA, label = r'$P$ in PBS Auction Setup', linewidth=4, color='purple', linestyle='-', marker = 'o', markersize=12)
    plt.plot(gammas, mean_proposerC, label = r'$P$ in MEV-Game', linewidth=4, linestyle='--', color='purple', marker = '^', markersize=12)

    plt.plot(gammas, avg_builderA, label=r'$\tilde{B}$ in PBS Auction Setup', linewidth=4, linestyle='-', color='blue', marker = 'o', markersize=12)
    plt.plot(gammas, avg_builderC, label=r'$\tilde{B}$ in MEV-Game', linewidth=4, linestyle='--', color='blue', marker = '^', markersize=12)
    
    plt.plot(gammas, avg_ofpA, label=r'$\tilde{O}$ in PBS Auction Setup', linewidth=4, linestyle='-', color='orange', marker = 'o', markersize=12)
    plt.plot(gammas, avg_ofpC, label=r'$\tilde{O}$ in MEV-Game', linewidth=4, linestyle='--', color='orange', marker = '^', markersize=12)
    plt.axvline(x=1.27, color='black', linestyle='--', linewidth=4)
    plt.xlabel(r'$\gamma$', fontsize=60)
    plt.ylabel('Utility', fontsize=60)
    plt.tick_params(axis='both', which='major', labelsize=50)
    # plt.legend(loc='center left', bbox_to_anchor=(1.2, 0.5), fontsize=15, frameon=False, framealpha=0.0)

    plt.tight_layout()
    plt.grid(False)
    plt.show()

def plot_vals_3(gammas, builders_list, num_ofas, distributions, list_valuesA, list_valuesC):
    for j in range(len(distributions)):
        for g in range(len(gammas)):
            plt.figure(figsize=(10, 8))
            mean_proposer_listA = []
            mean_builders_listA = []
            mean_ofas_listA = []

            mean_proposer_listC = []
            mean_builders_listC = []
            mean_ofas_listC = []

            for ind in range(len(builders_list)):
                (mean_proposerA, std_proposerA) = list_valuesA[ind][j][2]
                (mean_builderA, std_builderA) = list_valuesA[ind][j][1]
                (mean_ofaA, std_ofaA) = list_valuesA[ind][j][0]

                (mean_proposerC, std_proposerC) = list_valuesC[ind][j][2]
                (mean_builderC, std_builderC) = list_valuesC[ind][j][1]
                (mean_ofaC, std_ofaC) = list_valuesC[ind][j][0]

                mean_proposer_listA.append(np.mean(mean_proposerA[g]))
                mean_builders_listA.append(np.mean(mean_builderA[g]))
                mean_ofas_listA.append(np.mean(mean_ofaA[g]))

                mean_proposer_listC.append(np.mean(mean_proposerC[g]))
                mean_builders_listC.append(np.mean(mean_builderC[g]))
                mean_ofas_listC.append(np.mean(mean_ofaC[g]))

            plt.plot(builders_list, mean_proposer_listA, label = r'$P$ in PBS Auction Setup', color='purple', linestyle = '-', marker = 'o', linewidth=4, markersize=12)
            plt.plot(builders_list, mean_proposer_listC, label = r'$P$ in MEV-Game', color='purple', linestyle = '--', marker = '^', linewidth=4, markersize=12)

            plt.plot(builders_list, mean_builders_listA, label = r'$\tilde{B}$ in PBS Auction Setup', color='blue', linestyle = '-', marker ='o', linewidth=4, markersize=12)
            plt.plot(builders_list, mean_builders_listC, label = r'$\tilde{B}$ in MEV-Game', color='blue', linestyle = '--', marker = '^', linewidth=4, markersize=12)

            plt.plot(builders_list, mean_ofas_listA, label = r'$\tilde{O}$ in PBS Auction Setup', color='orange', linestyle = '-', marker = 'o', linewidth=4, markersize=12)
            plt.plot(builders_list, mean_ofas_listC, label = r'$\tilde{O}$ in MEV-Game', color='orange', linestyle = '--', marker = '^', linewidth=4, markersize=12)
                # for i, val in enumerate(mean_ofas_list[j]):
                #     plt.annotate(f'{val}', (builders_list[i+j], val), textcoords="offset points", xytext=(3,2), ha='center')

            # plt.title('Means of Revenue for Various Builders with ' +  str(num_ofas) + ' OFAs and ' + distributions[j] +' Distribution and Gamma = ' + str(gammas[2]))
            plt.xlim(2, builders_list[-1])
            # plt.ylim(min_vals-0.1, 1.4*max_vals)
            # plt.xticks(x_positions + offset*(3/2) , x_roles)
            plt.xlabel('Number of Builders', fontsize = 60)
            plt.ylabel('Utility', fontsize = 60)
            plt.tick_params(axis='both', which='major', labelsize=50)
            # plt.legend(loc='center left', bbox_to_anchor=(0.64, 0.69), fontsize=13.5, frameon=True, framealpha=0.0)

            plt.tight_layout()
            plt.grid(False)
            plt.show()

def violin_plot(proposerA, proposerC, builderA, builderC, ofaA, ofaC, num_iters, g, num_builders, num_ofas, gammas, type):
    x_proposer = [r'P']
    x_builders = [r'B']
    x_ofas = [r'O']

    x_roles = x_proposer + x_builders + x_ofas
    num_roles = len(x_roles)
    idx = 0
    builderA_vals = [row[idx] for row in builderA[g]]
    builderA_vals = np.array(builderA_vals).flatten()
    ofaA_vals = [row[idx] for row in ofaA[g]]
    ofaA_vals = np.array(ofaA_vals).flatten()

    builderC_vals = [row[idx] for row in builderC[g]]
    builderC_vals = np.array(builderC_vals).flatten()
    ofaC_vals = [row[idx] for row in ofaC[g]]
    ofaC_vals = np.array(ofaC_vals).flatten()

    data1 = pd.DataFrame({
    'Group': np.repeat(x_roles, num_iters),
    'Category': np.tile(np.repeat(['Auction'], num_iters), num_roles),
    'Value': np.concatenate([proposerA[g].flatten(), builderA_vals, ofaA_vals])
    })

    data2 = pd.DataFrame({
    'Group': np.repeat(x_roles, num_iters),
    'Category': np.tile(np.repeat(['Shapley'], num_iters), num_roles),
    'Value': np.concatenate([proposerC[g].flatten(), builderC_vals, ofaC_vals])
    })
    data = pd.concat([data1, data2], axis=0)
    plt.figure(figsize=(10, 8))

    sns.violinplot(x='Group', y='Value', hue='Category', data=data, split=True, inner = None, cut = 0)
    # sns.pointplot(x='Category', y='Value', data=data, linestyles=None, errorbar=None, color='black', markers='D')
    plt.legend(title='Setting', title_fontsize = 24, fontsize=22, framealpha = 0, bbox_to_anchor=(0.275, 0.85), loc='center left')
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Player', fontsize=30)
    plt.ylabel('Utility', fontsize=30)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.savefig(f'Figures/{num_builders}_Builders_{num_ofas}_OFAs_Distibution_{type}_violin_plot_Gamma_{gammas[g]}.pdf')
    # plt.show()
