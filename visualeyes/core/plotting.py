import pandas as pd
import numpy as np
from eyelinkio import read_edf
import matplotlib.pyplot as plt
import os
from .utility import dataframe_validation

def plot_as_scatter(data, screen_dimensions, aoi_definitions=None, save_png=None, save_path=None):
    """
    plot the data on the AOI mask, and optionally save the plot to the working directory as a PNG file.

    Inputs:
    - data: pd.DataFrame
    - screen dimensions: tuple
        (height, width)
    - aoi_definitions: list of dict or None
        Each dict defines one AOI (so we can have multiple) with keys:
        - 'shape': 'rectangle' or 'circle'.
        - 'coordinates': tuple of coordinates:
            - for rectangluar AOI's: (x1, x2, y1, y2), upper-bounds non-inclusive. 
            - for circlular AOI's: (x_center, y_center, radius).
    - save_png: bool or None
        If True, the results will be saved as png file(s)
    - save_path: str or None 
        
    Outputs:
    - fig, ax

    """

    # check if input data is a pd.DataFrame
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input data should be a pandas dataframe")
    
    # validate the input dataframe and save the x and y coordinates if the dataframe is valid
    x_coord, y_coord = dataframe_validation(data)

    # check if there are data outside screen dimension
    out_of_bounds_x = np.where((x_coord < 0) | (x_coord >= screen_dimensions[1]))[0] # list of indices
    out_of_bounds_y = np.where((y_coord < 0) | (y_coord >= screen_dimensions[0]))[0] # list of indices

    out_of_bounds = np.unique(np.concatenate([out_of_bounds_x, out_of_bounds_y]))

    clean_data = data.drop(index=out_of_bounds)

    fig, ax = plt.subplots()

    ax.set_xlim(0, screen_dimensions[1]-1)

    ax.set_ylim(0, screen_dimensions[0]-1)

    ax.set_ylim(ax.get_ylim()[::-1])

    ax.xaxis.tick_top()

    # plot scatter plot
    if 'axp' in clean_data.columns and 'ayp' in clean_data.columns:
        fixation_duration = []
        for _, series in clean_data.iterrows():
            single_duration = series['etime'] - series['stime']
            fixation_duration.append(single_duration)
        max_duration = round(max(fixation_duration), 2)
        mag_factor = [duration/max_duration for duration in fixation_duration]
        ax.scatter(clean_data['axp'], clean_data['ayp'], color='skyblue', marker='o', facecolors='none', s=[160 * mag for mag in mag_factor]) 
    else:
        ax.scatter(clean_data['xpos'], clean_data['ypos'], color='skyblue', marker='o', s=60)
    
    # optionally, overlay aoi
    if aoi_definitions is not None:
        # ax = visualeyes.aoi_contour
        pass

    if save_png:
        if not save_path:
            file_path = 'scatter_plot.png'
        else:
            file_path = os.path.join(save_path, 'scatter_plot.png')

        fig.savefig(file_path)
        print(f"Saved PNG file to {file_path}")

    return fig, ax