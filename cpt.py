import pandas as pd

class cp_table:

    def __init__(self, cols, row_names=[0]):
        self.table = pd.DataFrame(index=row_names, columns=cols)
        self.cols = cols
        self.rows = row_names

    def add_probabilities(self, probs):
        n_cols = len(self.cols)
        current_row = 0
        for i in range(0, len(probs), n_cols):
            row = self.rows[current_row]
            probabilities = probs[i:i+n_cols]
            self.table.loc[row] = probabilities
            current_row += 1
