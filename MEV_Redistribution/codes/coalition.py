import itertools

def are_entries_zero(tuple_data, i, j):
    # Check if all entries from index i to index j are 0
    for index in range(i, j + 1):
        if tuple_data[index] != 0:
            return False
    return True

def coalition_input(n, m, a, o):
    # Calculate the number of players
    # num_players = 1 + num_builders + num_ofas 
    num_players = 1 + n + m # Including proposer

    # Initialize a dictionary to store the utility of each coalition
    utility_dict = {}

    for i in range(2**num_players):
        coalition = tuple(int(bit) for bit in bin(i)[2:].zfill(num_players))
        if coalition[0] == 0: # If proposer is not in the coalition
            # Bit 0 of coalition is proposer
            utility_dict[coalition] = 0
        elif are_entries_zero(coalition, 1, n): # If all builders are not in the coalition
            # Bits 1 to n represent builders
            utility_dict[coalition] = 0
        else:
            utility_dict[coalition] = 0 # initialize utility to 0
            for j in range(1, n + 1): # Iterate over builders
                if coalition[j] == 1: # If builder j is in the coalition
                    utility_dict[coalition] = max(utility_dict[coalition], a[j - 1])
                    # take max of arbitrage valuation 
                    # over all builders in the coalition
            for k in range(n + 1, num_players): # Iterate over ofps
                if coalition[k] == 1: # If ofp belongs to coalition
                    u = 0 # Initialize utility of ofp to 0
                    for j in range(1, n + 1): # Iterate over builders
                        if coalition[j] == 1:
                            # If builder j is in the coalition
                            u = max(u, o[k - n - 1][j - 1]) 
                            # Take max of sandwich valuation 
                            # over all builders in the coalition
                    utility_dict[coalition] += u # Add the utility 
                    # of ofp to the coalition
                else:
                    u_in, u_out = 0, 0 # Initialize max bid of builders
                    # in and out of the coalition
                    for j in range(1, n + 1): # Iterate over builders
                        if coalition[j] == 1: # If builder j belongs
                            # to the coalition
                            u_in = max(u_in, o[k - n - 1][j - 1])
                            # take max
                        else: # If builder j doesnt belong to coalition
                            u_out = max(u_out, o[k - n - 1][j - 1])
                            # take max
                    utility_dict[coalition] += max(0, u_in - u_out)
                    # If u_in > u_out, coalition wins the auction;
                    # hence, add the profit (diff) to the coalition
                    # If not, add 0 to the coalition because coalition
                    # loses the auction
    return utility_dict

def factorial(n, fact):
    if n == 0:
        return 1
    fact[n] = n * factorial(n - 1, fact)
    return fact[n]

def initialize_tuple(tup, num_players):
    t = tuple(0 for _ in range(num_players))
    for idx in tup:
        t = t[:idx] + (1,) + t[idx + 1:]
    return t

def calculate_shapley_value(n, m, a, o):
    utility_dict = coalition_input(n, m, a, o)
    num_players = 1 + n + m
    fact = [1] * (num_players + 1)
    factorial(num_players, fact)
    shapley_values = [0] * num_players
    for perm in itertools.permutations(range(num_players), num_players):
        for player in range(num_players):
            i = perm.index(player)
            with_player = initialize_tuple(perm[:i + 1], num_players)
            without_player = initialize_tuple(perm[:i], num_players)
            marginal_value = utility_dict[with_player] - utility_dict[without_player]
            shapley_values[player] += marginal_value

    num_players_fact = fact[num_players]
    shapley_values = [value / num_players_fact for value in shapley_values]

    return shapley_values

