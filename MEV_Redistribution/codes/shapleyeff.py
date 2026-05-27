import numpy as np

def factorial(n, fact): # Calculates factorial of 
    # numbers from 0 to n and stores it
    if n == 0:
        return 1
    fact[n] = n * factorial(n - 1, fact)
    return fact[n]

def calculate_SV_eff(n, m, a, o):
    # n = number of builders
    # m = number of orders
    # a = list of values of arbitrage valuations
    # o = list of values of order flow valuations (m x n)
    # jth row of o represents the order flow valuations 
    # of n builders in jth order
    num_players = 1 + n + m # proposer + num_builders + num_orders
    fact = [1] * (num_players + 1) # initializes factorial array with 1 each
    factorial(num_players, fact) # Calculates factorial of each index/number
    shapley_values = [0] * num_players 
    # initializes shapley values with 0 each
    # first(0 index) shapley value is of proposer
    # second(index 1) to (n + 1)-th (index n) shapley values are of builders
    # (n + 2)-th (index n + 1) to (n + m + 1)-th (index n + m) 
    # shapley values are of order flow providers
    assorted = np.argsort(-a) # sorts arbitrage valuations 
    # in descending order
    assorted_copy  = assorted # copy of assorted
    ao = np.vstack([a, o]) # combined arbitrage and order flow valuations array
    # note first row is arbitrage valuations
    # and next m rows are order flow valuations
    ao = ao[:,assorted] # sorts ao in descending order of arbitrage valuations
    # print(ao)
    sigma = np.zeros_like(o) # sigma[j][i] = rank of ith builder in jth order
    phi = np.zeros_like(o) # phi[j][i] = maps ith rank in jth order
    # to builder index 
    # sigma, phi are (m x n) arrays
    for j in range(1, m + 1): # iterating over orders
        assorted = np.argsort(-ao[j]) # sorts order flow valuations
        for i in range(n): # iterating over builders
            sigma[j - 1][assorted[i]] = i # maps builder index to rank
            phi[j - 1][i] = assorted[i] # maps rank to builder index
    # shapley values of order flow provider j 
    for j in range(n + 1, n + m + 1): # iterating over order flow providers
        # Finding Shapley Value of O_{j-n}
        ans = 0
        for i in range(2, n + 1): # iterating over builders
            ans += ao[j - n][int(phi[j - n - 1][i - 1])] / (i * (i + 1))
            # eq. 5
        shapley_values[j] = ans
    # shapley value of proposer
    shap_val_prop = 0
    for i in range(1, n + 1): # iterating over builders
        shap_val_prop += ao[0][i - 1] / (i * (i + 1)) # eq. 13
    for j in range(m): # iterating over order flow providers
        shap_val_prop += ao[j + 1][int(phi[j][0])] / 2 # eq. 13
    shapley_values[0] = shap_val_prop # ans
    # shapley values of builders
    for k in range(1, n + 1): # Finding shapley value of B_k
        delta, epsilon, lamda_1, lamda_2 = 0, 0, 0, 0
        for i in range(1, n - k + 1): # 1 -> (n - k)
            delta += 2 * (ao[0][k - 1] - ao[0][k - 1 + i]) / ((k + i - 1) * (k + i) * (k + i + 1))
        delta += ao[0][k - 1] / (n * (n + 1))
        # eq. 14
        for j in range(1, m + 1): # 1 -> m
            k_ = int(sigma[j - 1][k - 1]) + 1 # k_ = rank of kth builder in jth order
            for i in range(1, n - k_ + 1): # 1 -> (n - k_)
                epsilon += 2 * 3 * (ao[j][k - 1] - ao[j][int(phi[j - 1][k_ + i - 1])]) / ((k_ + i - 1) * (k_ + i) * (k_ + i + 1) * (k_ + i + 2))
            epsilon +=  2 * ao[j][k - 1] / (n * (n + 1) * (n + 2))
        # eq. 15

        for j in range(1, m + 1): # 1 -> m
            k_ = int(sigma[j - 1][k - 1]) + 1 # k_ = rank of kth builder in jth order
            for i in range(1, n - k_ + 1): # 1 -> (n - k_)
                lamda_2 += 2 * (ao[j][k - 1] - ao[j][int(phi[j - 1][k_ + i - 1])]) / ((k_ + i) * (k_ + i + 1) * (k_ + i + 2))
            lamda_2 += ao[j][k - 1] / ((n + 1) * (n + 2))
        # eq. 21
        shapley_values[assorted_copy[k - 1] + 1] = delta + epsilon + lamda_2
        # eq. 22
        # maps back to original builder index (given by user)
    return shapley_values

# # Example usage
# n = 2
# m = 1
# a = np.array([6, 5])
# o = np.zeros((m, n))
# o[0][0] = 7
# o[0][1] = 10

# shapley_values = calculate_SV_eff(n, m, a, o)
# print("Shapley Values:", shapley_values)