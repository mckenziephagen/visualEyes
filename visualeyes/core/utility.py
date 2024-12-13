import pandas as pd
import numpy as np
import numbers

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
        # pull the x and y coordinates
        if 'axp' in df.columns and 'ayp' in df.columns:
            x_coord = df['axp']
            y_coord = df['ayp']
        else:
            x_coord = df['xpos']
            y_coord = df['ypos']
            
    return (x_coord.values, y_coord.values)

def aoi_definitions_validation(aoi_definitions, screen_dimensions):
    """
    Validate the input AOI definitions
    
    Parameters:
    -----------
    aoi_definitions : dict, list of dict, or numpy.ndarray of dict
        The AOI definitions to overlay on the plot. Each dict should contain:
        - 'shape': 'rectangle' or 'circle'.
        - 'coordinates': tuple, list or np.ndarray of coordinates.
            - for rectangluar AOI's: (x1, x2, y1, y2), upper-bounds non-inclusive. 
            - for circlular AOI's: (x_center, y_center, radius).
    screen_dimensions : tuple
        The dimensions of the screen in pixels (height, width).
        
    Returns:
    --------
    None
    """
    # check if aoi_definitions is not empty
    if not aoi_definitions:
        raise ValueError('AOI definitions cannot be empty')

    # check if aoi_definitions is a dictionary, list, or numpy array
    if not isinstance(aoi_definitions, (dict, list, np.ndarray)):
        raise ValueError('AOI definitions should be a dictionary or a list of dictionaries')
    
    # check if aoi_definitions is a list of dictionaries
    if isinstance(aoi_definitions, (list, np.ndarray)):
        if any([not isinstance(aoi, dict) for aoi in aoi_definitions]):
            raise ValueError('AOI definitions should be a list of dictionaries')
    
    # check if aoi_definitions is a dictionary
    if isinstance(aoi_definitions, dict):
        # convert the dictionary to a list
        aoi_definitions = [aoi_definitions]
    
    for aoi in aoi_definitions:
        
        # check if the required keys are present in the dictionary
        required_keys = ['shape', 'coordinates']
        missing_keys = [key for key in required_keys if key not in aoi.keys()]
        if missing_keys:
            raise KeyError(f'Missing keys in AOI definition: {missing_keys}')
        
        # check if the 'shape' key has a valid value
        if aoi['shape'] not in ['rectangle', 'circle']:
            raise ValueError(f'Unsupported AOI shape: {aoi['shape']}')
        
        # check if the 'coordinates' key corresponds to a tuple, list, or numpy array
        if not isinstance(aoi['coordinates'], (tuple, list, np.ndarray)):
            raise ValueError('AOI coordinates should be a tuple, list, or numpy array')
        
        # check if the 'coordinates' key has the correct number of elements
        if aoi['shape'] == 'rectangle' and len(aoi['coordinates']) != 4:
            raise ValueError('Rectangle coordinates should have four elements')
        
        elif aoi['shape'] == 'circle' and len(aoi['coordinates']) != 3:
            raise ValueError('Circle coordinates should have three elements')
        
        # check if the 'coordinates' key has valid values (non-negative integers)
        if not all(isinstance(coord, (numbers.Integral)) for coord in aoi['coordinates']):
            raise ValueError('All coordinates must be integers')
        
        if any(coord < 0 for coord in aoi['coordinates']):
            raise ValueError('Coordinates cannot be negative')
        
        # check if the 'coordinates' key is within the screen boundaries
        screen_height, screen_width = screen_dimensions

        if aoi['shape'] == 'rectangle':
            x1, x2, y1, y2 = aoi['coordinates']
            
            if x1 > x2:
                raise ValueError('x1 cannot be greater than x2')
            if y1 > y2:
                raise ValueError('y1 cannot be greater than y2')
            
            if x2 > screen_width or y2 > screen_height:
                raise ValueError('AOI exceeds screen boundaries')
                    
        elif aoi['shape'] == 'circle':
            x_center, y_center, radius = aoi['coordinates']
    
            if (x_center - radius < 0 or x_center + radius > screen_width or
                y_center - radius < 0 or y_center + radius > screen_height):
                raise ValueError('AOI exceeds screen boundaries')
        
    return None

def screen_dimensions_validation(screen_dimensions):
    
    '''
    Validate the screen dimensions
    
    Parameters:
    -----------
    screen_dimensions : tuple, list, or numpy.ndarray
        Screen dimensions (height, width)
        
    Returns:
    --------
    None
    '''
    
    # check if screen_dimensions is a tuple
    if not isinstance(screen_dimensions, (tuple, list, np.ndarray)):
        raise ValueError('Screen dimensions should be a tuple, list, or numpy array')
    
    # check if screen_dimensions has two elements
    if len(screen_dimensions) != 2:
        raise ValueError('Screen dimensions should have two elements.')
    
    # check if screen_dimensions has positive integer values
    if not all(isinstance(dim, numbers.Integral) for dim in screen_dimensions):
        raise ValueError('Screen dimensions should have positive integer values.')
    
    if any(dim <= 0 for dim in screen_dimensions):
        raise ValueError('Screen dimensions should have positive integer values.')
    
    return None