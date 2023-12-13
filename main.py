from Auction.auction import win

try:
    # Get the number of builders, searchers, and OFAs from the user
    num_builders = int(input("Enter the number of Builders: "))
    num_searchers = int(input("Enter the number of Searchers: "))
    num_ofas = int(input("Enter the number of OFAs: "))
    
    # Print the number of builders, searchers, and OFAs
    print(f"Number of Builders: {num_builders}")
    print(f"Number of Searchers: {num_searchers}")
    print(f"Number of OFAs: {num_ofas}")

    # Initialize an empty dictionary to store searcher valuations for each OFA
    searcher_valuations = {}
    
    # Loop through each OFA
    for ofa in range(1, num_ofas + 1):
        # Initialize a list to store searcher valuations (which is equal to their bid) for this OFA
        ofa_bids = []
        
        # Loop through each searcher in this OFA
        for searcher in range(1, num_searchers + 1):
            valuation = float(input(f"Enter the valuation of Searcher {searcher} in OFA {ofa}: "))
            ofa_bids.append(valuation)
        
        # Store the list of searcher valuations for this OFA in the dictionary
        searcher_valuations[ofa] = ofa_bids

    searcher_utilities, builder_utilities = win(num_builders=num_builders, num_searchers=num_searchers, num_ofas=num_ofas, searcher_valuations=searcher_valuations)
    print(searcher_utilities, builder_utilities)
except ValueError:
    print("Please enter valid integer values for the number of builders, searchers, and OFAs.")
