import xarray as xr
import numpy as np

class cp_table:

    """
    data = np.zeros((3,2,2))
    dims = ["A", "E", "S"]
    a = ...
    e = ...
    s = ...
    coords = [a, e, s]
    foo = xr.DataArray(data, coords=coords, dims=dims)
    """

    def __init__(self, data, dims, coords):
        dimension = []
        for c in coords:
            dimension.append(len(c))
        dimension = tuple(dimension)

        data = np.array(data)
        rshaped_data = np.reshape(data, dimension)

        if rshaped_data.size != data.size:
            print("Wrong shape given. Data was lost.")
            SystemError(0)

        self.table = xr.DataArray(rshaped_data, coords=coords, dims=dims)
        self.dimension = dimension

    def __repr__(self):
        return self.table.__repr__()

    def __eq__(self, other):
        return self.table == other.table
