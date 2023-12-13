def compute_builder_utilities(winners, builder_utilities):
    # Loop through each searcher bundle
    for searcher, ofas_won in winners.items():
        for ofa in ofas_won:
            # Increment the utility of the builder for every bundle searcher gives him
            builder_utilities[1] += 1

def win(num_builders, num_searchers, num_ofas, searcher_valuations):
    # Initialize dictionaries to store the utilities of each searcher and builder respectively
    searcher_utilities = {}
    builder_utilities = {}

    # Initialize a dictionary to store the OFAs won by each searcher
    winners = {}

    # Initialize all builders to have a utility of 0
    for builder in range(1, num_builders + 1):
        if builder not in builder_utilities:
            builder_utilities[builder] = 0

    # Intialize all searchers to have a utility of 0
    for searcher in range(1, num_searchers + 1):
        if searcher not in searcher_utilities:
            searcher_utilities[searcher] = 0

    # Iterate through each OFA and find the searcher with the highest valuation
    for ofa, ofa_bids in searcher_valuations.items():
        # Find the highest bid
        max_valuation = max(ofa_bids)
        
        # Find the index of the winning searcher
        max_valuation_index = ofa_bids.index(max_valuation)
        ofa_bids.remove(max_valuation)

        # Find the second-highest bid that the winning searcher has to pay
        bid = max(ofa_bids)

        # Insert the maximum bid back into the list
        ofa_bids.insert(max_valuation_index, max_valuation)

        # Add 1 to convert index to searcher number (assuming searcher numbering starts from 1)
        winning_searcher = max_valuation_index + 1
        
        # Map searcher to the OFA they have won
        if winning_searcher not in winners:
            winners[winning_searcher] = [ofa]
        else:
            winners[winning_searcher].append(ofa)

        # Calculate utility and store it in the searcher_utilities dictionary
        utility = max_valuation - bid
        searcher_utilities[winning_searcher] += utility
        
        print(f"The Searcher {winning_searcher} wins OFA {ofa} with a utility of {utility}")

    compute_builder_utilities(winners=winners, builder_utilities=builder_utilities)
    
    return searcher_utilities, builder_utilities