import numpy as np

def calculate_vcg(v_ofa, v_pbs):

    utility = np.zeros(v_pbs.shape[0])
    payments_ofa = np.zeros(v_ofa.shape[0])
    payments_builders_to_ofa  = np.zeros(v_pbs.shape)
    #OFA
    h_ofas = np.zeros(v_ofa.shape[0], dtype=int)

    for i in range(v_ofa.shape[0]):
        sort_index_v_ofa = np.argsort(v_ofa[i])
        h_ofa = sort_index_v_ofa[-1]
        sh_ofa = sort_index_v_ofa[-2]

        h_ofas[i] = h_ofa

        payments_builders_to_ofa[h_ofa] += v_ofa[i][sh_ofa]

        payments_ofa[i] = v_ofa[i][sh_ofa]
        
        utility[h_ofa] += v_ofa[i][h_ofa] - v_ofa[i][sh_ofa] 


    #PBS
    vt_pbs = utility + v_pbs      
    
    h_pbs = None
    sh_pbs = None
    sort_index_vt_pbs = np.argsort(vt_pbs)
    h_pbs = sort_index_vt_pbs[-1]
    sh_pbs = sort_index_vt_pbs[-2]
    
    winner_pbs = np.zeros(v_pbs.shape)
    winner_pbs[h_pbs] = 1

    payment_pbs =  vt_pbs[sh_pbs]

    utility = np.multiply(winner_pbs, vt_pbs[h_pbs] - vt_pbs[sh_pbs]) - np.multiply(1 - winner_pbs, payments_builders_to_ofa)
  

    return h_ofas, h_pbs, utility, payment_pbs, payments_ofa

