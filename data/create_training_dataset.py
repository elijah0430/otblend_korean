import pandas as pd
import ast
from itertools import combinations

with open("otblend_data.csv", encoding="UTF8") as file:
    df=pd.read_csv(file)




def compare_hierarchical_scores(score1, score2):
    """Compare two hierarchical scores according to the hierarchy.
    Return -1 if score1 is better than score2,
    Return 1 if score1 is worse than score2,
    Return 0 if they are equal.
    """
    for v1, v2 in zip(score1, score2):
        if v1 < v2:
            return -1  # score1 is better
        elif v1 > v2:
            return 1   # score1 is worse
    return 0  # scores are equal

# Initialize an empty list to store the new rows
new_rows = []

# Iterate over each row in the DataFrame
for idx, row in df.iterrows():
    word1 = row['Word1']
    word2 = row['Word2']
    # Safely evaluate the Order_Candidates string to a Python object
    order_candidates = ast.literal_eval(row['Order_Candidates'])
    # Prepare a list of candidates and their hierarchical scores
    candidates = []
    for candidate, hierarchical_score in order_candidates:
        candidates.append((candidate, hierarchical_score))
    # Generate all possible pairs of candidates
    for cand1, cand2 in combinations(candidates, 2):
        candidate1, score1 = cand1
        candidate2, score2 = cand2
        comparison = compare_hierarchical_scores(score1, score2)
        if comparison == -1:
            # candidate1 is better than candidate2
            accepted_candidate = candidate1
            unaccepted_candidate = candidate2
        elif comparison == 1:
            # candidate2 is better than candidate1
            accepted_candidate = candidate2
            unaccepted_candidate = candidate1
        else:
            # Candidates are equal, skip this pair
            continue
        # Append a new row with Word1, Word2, accepted and unaccepted candidates
        new_rows.append({
            'Word1': word1,
            'Word2': word2,
            'Accepted_Candidate': accepted_candidate,
            'Unaccepted_Candidate': unaccepted_candidate
        })

# Create a new DataFrame from the new rows
new_df = pd.DataFrame(new_rows)

new_df.to_csv("otblend_train_data.csv")

print(new_df)
