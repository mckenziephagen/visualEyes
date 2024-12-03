# Component 1: EDF File I/O
## Purpose:
- convert an EDF file to dataframes

## Input:
- one EDF file

## Output:
- a dictionary of pandas dataframes each contains different information parsed out of the EDF file

## Other components used: N/A

# Component 2: Define Experiment Variables

## Purpose:
- define a couple of variables potentially used in other components in one place

## Input:
- experiment screen resolution
	- optional, could infer from eyelink output
- viewing distance 
	- optional, to compute number of pixels corresponding to a certain degree of visual angle
- trial information (necessary?)
	- start time of each trial of the experiment in seconds (list/np.array)
	- end time of each trial of the experiment in seconds (list/np.array)
	- duration of trial
		- optional. If trial end time was not provided, compute using start time and duration. Could be either one number or a list/np.array of numbers that has equal length with start time.
	- **issue**: Trial information can be used when creating epochs, which can then be used to select samples of interest from the data. E.g. if we know the onsets of all trials, and users want to investigate data 0.3s after trial onset, we can easily compute that. However this approach is not so flexible, e.g. what if people want to look at data at 0.3s before trial onset?(might need a seperate parameter for that); what if the length of epoch differs based on trial type, etc. For flexibility, is it better to have the users define the start and end of epochs themselves (hence trial information is unnecessary)?

## Output:
- a dictionary containing relevant information for the use of other components

## Other components used:
- Component 1 if users don't provide screen resolution

# Component 3: Create epochs


# Component 4: Define area of interest on the screen

## Purpose:
- define area of interest on the screen that will be used for plotting and thresholding

## Input:
- x and y coordinates of the AOI centers (tuple or list of tuples if multiple AOI)
- spread of the AOI from the center (pixels/degree of visual angle, either float or a list of float that has same length with the number of x and y coords provided)

## Output:
- a 2D binary mask that has shape y resolution * x resolution, where AOI is flagged with 1 and the rest 0.

## Other components used:
- N/A

# Component 5: Plot heatmap of eye-tracking data

## Purpose:
- visualize eye-tracking data

## Input:
- dataframe containing relevant data
- AOI mask (optional)

## Output:
- a heatmap reflecting looking behavior
- if AOI mask is provided, overlay the AOI onto heatmap

## Other component used:
- data from Component 1
- screen specs from Component 2 (optional)
- AOI from Component 3 (optional)