


from itertools import combinations




# Calculate support for a given itemset in the transactions
def get_support(itemset, transactions):
    count = 0
    for transaction in transactions:
        if itemset.issubset(transaction):
            count += 1
    return count / len(transactions)




# Generate initial 1-item candidates from transactions
def get_initial_candidate(transactions):
    items = set()
    for transaction in transactions:
        for item in transaction:
            items.add(item)
    # Create a list of single-item sets
    candidates = [{item} for item in items]
    return candidates






# Filter candidates based on minimum support threshold
def support_filter(candidates_supports, minsup):
    filtered_candidates = []
    for itemset, support in candidates_supports.items():
        if support >= minsup:
            filtered_candidates.append(itemset)
    return filtered_candidates





# Generate new candidate itemsets by combining existing ones
def get_new_candidates(k, candidates):
    new_candidates = []
    for a in candidates:
        for b in candidates:
            # Union of two sets to create a new candidate
            union_set = a.union(b)
            # Ensure only sets of size k are added
            if len(union_set) == k and union_set not in new_candidates:
                new_candidates.append(union_set)
    return new_candidates




# Generate association rules from frequent itemsets-------
def get_association_rules(frequent_itemsets , minconf):
    rules=[]
    for itemset in frequent_itemsets:
        # Rules can only be generated from itemsets with more than one element
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = set(antecedent)
                    consequent = set(itemset) - antecedent
                    if consequent:
                        # Calculate confidence for the rule
                        confidence = get_support(itemset, transactions) / get_support(antecedent, transactions)
                        if confidence >= minconf:
                            rules.append((antecedent, consequent, confidence))
    return rules




def apriori(transactions, minsup, minconf):
    # Generate initial candidate 1-itemsets
    candidates = get_initial_candidate(transactions)

    frequent_itemsets = []  # To store all frequent itemsets
    k = 1  # Start with 1-itemsets
    rules = []  # To store generated association rules

     #--------------------------tart ITERATION---------------

    while candidates:
        # Calculate support for each candidate itemset
        candidates_supports = {}
        for itemset in candidates:
            candidates_supports[frozenset(itemset)] = get_support(itemset, transactions)

        filtered_candidates = support_filter(candidates_supports, minsup)

        # Stop if no candidates are left
        if not filtered_candidates:
            break

        frequent_itemsets.extend(filtered_candidates)

        # Generate new candidates for the next iteration
        k += 1
        candidates = get_new_candidates(k, filtered_candidates)
        
    #--------------------------End ITERATION---------------
    rules = get_association_rules(frequent_itemsets ,minconf)

    return frequent_itemsets, rules




transactions = [
        {"Bread", "Milk"},
        {"Bread", "Diapers", "Cola", "Eggs"},
        {"Milk", "Diapers", "Cola", "Coffee"},
        {"Bread", "Milk", "Diapers", "Cola"},
        {"Bread", "Milk", "Diapers", "Coffee"},
 
    ]
min_support = 0.4  # Minimum support threshold
min_confidence = 0.4  # Minimum confidence threshold

frequent_itemsets, rules = apriori(transactions, min_support, min_confidence)

print("Frequent Itemsets:")
for itemset in frequent_itemsets:
    print(itemset)

print("\nAssociation Rules:")
for rule in rules:
    antecedent, consequent, confidence = rule
    print(f"{antecedent} => {consequent} (Confidence: {confidence:.2f})")





