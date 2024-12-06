import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import visualeyes
import eyelinkio

def test_define_aoi(): 
    edf_path = os.path.join('data', 'TG_2015.EDF')
    
    edf = eyelinkio.read_edf(edf_path)
    
    screen_coords = edf['info']['screen_coords']
    screen_width = int(screen_coords[1])
    screen_height = int(screen_coords[0])
    
    aoi_definitions = [{'shape':'rectangle', 'coordinates': ('462', '590', '563', '691')}]
    
    mask = visualeyes.define_aoi(screen_width, screen_height, aoi_definitions) 
