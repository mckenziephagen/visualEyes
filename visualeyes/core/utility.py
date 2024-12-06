import eyelinkio

def add_time_to_sample(edf, edf_dfs):
    
    '''
    Add time to the "sample" dataframe
    
    Parameters:
    -----------
    edf_dfs : dict
        dictionary of pandas dataframes from eyelinkio.EDF.to_pandas() output
    edf: eyelinkio.edf.EDF
        eyelinkio.edf.EDF object
        
    Returns:
    --------
    edf_dfs : dict
        dictionary of pandas dataframes from eyelinkio.EDF.to_pandas() output with 
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