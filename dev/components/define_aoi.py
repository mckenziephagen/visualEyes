import numpy as np

def define_aoi(screen_width, screen_height, aoi_definitions):
    """
    Define Areas of Interest (AOIs).
    
    Inputs:
    - screen_width (int): Width of the screen in pixels.
    - screen_height (int): Height of the screen in pixels.
    - aoi_definitions (list of dict): Each dict defines one AOI (so we can have multiple) with keys:
        - 'shape': 'rectangle' or 'circle'.
        - 'coordinates': Tuple of coordinates:
            - For rectangluar AOI's: (x1, y1, x2, y2), upper-bounds non-inclusive. 
            - For circlular AOI's: (x_center, y_center, radius).
    - visual_angle (dict, optional): Info to convert visual angles to pixels.
        Keys might include 'eye_to_screen_distance' and 'screen_resolution'.

    Output:
    - mask (2D numpy array): Binary mask of the AOIs
    """
    #Check inputs 
    if not isinstance(screen_width, int):
        raise ValueError("Screen width coordinates must be integers.")

    if not isinstance(screen_height, int):
        raise ValueError("Screen height coordinates must be integers.")

    if screen_width <= 0 or screen_height <= 0:
        raise ValueError("Screen dimensions must be positive.")

    if not isinstance(aoi_definitions, list):
        raise ValueError("AOI coordinates must be a list of dictionaries.")

    #Initialize a mask
    mask = np.zeros((screen_height, screen_width), dtype=np.uint8)

    #Define each AOI
    for aoi in aoi_definitions:
        shape = aoi['shape'].lower()
        coordinates = aoi['coordinates']
        
        if shape == 'rectangle':
        
            x1, y1, x2, y2 = map(int, coordinates) #Convert to integers
            mask[y1:y2, x1:x2] = 1  #All pixels within the rectangle are 1
            if x1 < 0 or y1 < 0 or x2 > screen_width or y2 > screen_height:
                raise ValueError(f"Coordinates exceed screen boundaries.")
        elif shape == 'circle':
            x_center, y_center, radius = map(int, coordinates) #Convert to integers
            if x_center - radius < 0 or y_center - radius < 0 or center_x + radius > screen_width or center_y + radius > screen_height:
                raise ValueError(f"Circle exceeds screen boundaries.")
            for y in range(screen_height):
                for x in range(screen_width):
                    # Use the equation of a circle to check if (x, y) is inside
                    if (x - x_center)**2 + (y - y_center)**2 <= radius**2:
                        mask[y, x] = 1 #All pixels within the circle are 1
        else:
            raise ValueError(f"Unsupported AOI shape: {shape}")
    
    return mask
