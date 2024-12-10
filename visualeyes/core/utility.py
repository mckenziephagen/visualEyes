import eyelinkio
import pandas as pd
import numpy as np

def add_time_to_sample(edf, edf_dfs):
    
    '''
    Add time to the "sample" dataframe
    
    Parameters:
    -----------
    edf_dfs : dict
        Dictionary of pandas dataframes from eyelinkio.EDF.to_pandas() output
    edf: eyelinkio.edf.EDF
        eyelinkio.edf.EDF object
        
    Returns:
    --------
    edf_dfs : dict
        Dictionary of pandas dataframes from eyelinkio.EDF.to_pandas() output with 
        time column added to the "sample" dataframe
    '''
    
    # check if edf_dfs is a dictionary of dataframes
    if not isinstance(edf_dfs, dict):
        raise ValueError('edf_dfs should be a dictionary of dataframes')
    
    # check if sample dataframe is in the dictionary
    if 'samples' not in edf_dfs.keys():
        raise ValueError('samples dataframe is not in the dictionary')
    
    # check if edf is an eyelinkio.edf.EDF object
    if not isinstance(edf, eyelinkio.edf.EDF):
        raise ValueError('edf should be an eyelinkio.edf.EDF object')
    
    # check if edf contains time column
    if 'times' not in edf.keys():
        raise ValueError('data should contain a time column')
    
    # add time to the "sample" dataframe
    edf_dfs['samples']['time'] = edf['times']
    
    return edf_dfs

def aoi_mask_validation(aoi_mask, screen_dimension):
    
    '''
    Validate the Area of Interest (AOI) mask
    
    Parameters:
    -----------
    aoi_mask : numpy.ndarray
        Binary mask of the AOI (shape: height x width)
    screen_dimension : tuple
        Screen dimension (width, height)
        
    Returns:
    --------
    None
    
    '''
    
    # check if aoi_mask is a numpy array
    if not isinstance(aoi_mask, np.ndarray):
        raise ValueError('AOI mask should be a numpy array')
    
    # check if aoi_mask is a 2D array
    if len(aoi_mask.shape) != 2:
        raise ValueError('AOI mask should be a 2D array')
    
    # check if aoi_mask is a binary mask
    if not np.all(np.isin(aoi_mask, [0, 1])):
        raise ValueError('AOI mask should be a binary mask')
    
    # check if aoi_mask has the same shape as the screen dimension
    if aoi_mask.shape != screen_dimension:
        raise ValueError('AOI mask should have the same shape as the screen dimension')

    return None


def dataframe_validation(df):
        
    '''
    Validate the input dataframe and return the x and y coordinates if the dataframe is valid
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    x_coord : numpy.ndarray
        x coordinates
    y_coord : numpy.ndarray
        y coordinates
    '''
    x_coord = None
    y_coord = None
    
    # check if input data is a pd.DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError('input data should be a pandas dataframe')
    
    # check if the dataframe contains either 'axp' and 'ayp' or 'xpos' and 'ypos' columns
    if not (('axp' in df.columns and 'ayp' in df.columns) or ('xpos' in df.columns and 'ypos' in df.columns)):
        raise ValueError('missing x and y coordinates')
    
    else:
        if 'axp' in df.columns and 'ayp' in df.columns:
            x_coord = df['axp']
            y_coord = df['ayp']
        else:
            x_coord = df['xpos']
            y_coord = df['ypos']

    return (x_coord.values, y_coord.values)