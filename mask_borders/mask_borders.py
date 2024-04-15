import numpy as np

def mask_borders(data_og, border = 10):

    '''
    Mask borders of image in FITS file for source detection. The no-data regions
    of the image must be set to NaN for this function to work.
    This function will provide a rough mask of the borders for source detection,
    but since it does this row-by-row (and column-by-column), the masked
    border will ve very jagged. 

    Parameters
    ----------
    data_og - numpy array
        The data associated with the FITS file
    border - float
        The pixel size of the border that will be masked
    '''

    data = np.copy(data_og)

    # Add border that you will remove later
    data = np.pad(data, pad_width=border, mode='constant', constant_values=np.nan)

    # Make array where Nan = False and Number = True
    bool_data = (data == data)

    # Make array that shows where NaN becomes Number or Number becomes NaN
    # True --> nan to num or num to nan
    col_diff = np.diff(bool_data, axis = 0) #cols
    row_diff = np.diff(bool_data, axis = 1) #rows

    # Find indices where NaN becomes number using col_diff and  row_diff
    w_col_transition = np.where(col_diff == True)
    w_row_transition = np.where(row_diff == True)

    for i in range(1, border+1):

        ### Right and Bottom borders ###
        w_col1 = (w_col_transition[0]-(i-1), w_col_transition[1])
        w_row1 = (w_row_transition[0], w_row_transition[1]-(i-1))
        # Set all places where NaN becomes a number to NaN to mask the borders
        # However, this will only mask the bottom or right-most borders becomes w_col and w_row
        # indicate the index BEFORE the transition happens
        data[w_col1] = np.nan
        data[w_row1] = np.nan

        ### Left and top borders ###
        # To get the indices after the transition happens (for masking top and right-most section):
        w_col2 = (w_col_transition[0]+i, w_col_transition[1])
        w_row2 = (w_row_transition[0], w_row_transition[1]+i)

        data[w_col2] = np.nan
        data[w_row2] = np.nan

    # Get rid of border you added at the beginning 
    data = data[border:-border, border:-border]

    # Need to do this so this data works with SEP
    data=np.ascontiguousarray(data)

    return data