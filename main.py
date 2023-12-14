from Auction.auction import utility_computation

try:
    
    def start():
        # Get the number of builders, searchers, and OFAs from the user
        num_builders = int(input("Enter the number of Builders: "))
        num_searchers = int(input("Enter the number of Searchers: "))
        num_ofas = int(input("Enter the number of OFAs: "))

        searcher_valuations = input_searcher_valuations({}, num_ofas, num_searchers)

        builder_valuations = input_builder_valuations({}, num_builders, num_searchers)
        
        searcher_utilities, builder_utilities = utility_computation(num_builders, num_searchers, num_ofas, builder_valuations, searcher_valuations)
        
        print(searcher_utilities, builder_utilities)
    
    def input_searcher_valuations(searcher_valuations, num_ofas, num_searchers):
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
        return searcher_valuations
    
    def input_builder_valuations(builder_valuations, num_builders, num_searchers):
        # Loop through each builder
        for builder in range(1, num_builders + 1):
            # Initialize a list to store valuations for each searcher with this builder
            searcher_valuations = []
            
            # Loop through each searcher
            for searcher in range(1, num_searchers + 1):
                valuation = float(input(f"Enter the valuation of Builder {builder} for Searcher {searcher}: "))
                searcher_valuations.append(valuation)
            
            # Store the list of valuations for this builder in the dictionary
            builder_valuations[builder] = searcher_valuations
        return builder_valuations
    
    start()
except ValueError:
    print("Please enter valid integer values for the number of builders, searchers, and OFAs.")
