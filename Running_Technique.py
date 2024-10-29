# by Edilson Borba 
# borba.edi@gmail.com

"""
# Running Classification Script

## Overview:
This script processes kinematic data (position, angle, and marker data) from an athlete's motion analysis, applies filtering, and then classifies the athlete as "Aerial" or "Terrestrial" based on specific criteria derived from the angles and foot positions at touch-down (TD) events.

## Workflow:
1. **Input Data**:
   - The script expects data in `.sto` and `.trc` file formats, containing global position, angle, and marker data.
   - The files should include "10" in their names and must be located in the appropriate subdirectories within the provided path.

2. **Low-Pass Filtering**:
   - The raw data is passed through a low-pass Butterworth filter to remove high-frequency noise. The cut-off frequency and filter order can be adjusted in the parameters.

3. **Touch-Down and Take-Off Event Detection**:
   - Using the heel-sacrum distance, peaks in the data are identified to mark touch-down (TD) and take-off (TO) events for both legs.

4. **Angle and Position Extraction**:
   - Hip and knee flexion angles are extracted at each TD event.
   - The foot position relative to the pelvis is calculated for further classification.

5. **Athlete Classification**:
   - Based on the average hip flexion and knee flexion angles, and foot position at TD, the athlete is classified

## Parameters:
- `Input`: Directory path where the data is stored.
- `Output`: Directory where the processed results are saved (currently not implemented in this version).

## Example Usage:
To use this script, update the `Path` and `Name` variables to point to the correct folder with your athlete's data, and run the script. The classification will be printed at the end of execution.
"""

# Paths and parameters
Path = 'path'
Name = 'name'
Output = 'oputput'

# Low-pass filter parameters
cutoff = 6  # Cut-off frequency in Hz
order = 3  # Filter order

Input = Path + Name + '/'

# Import libraries
import pandas as pd
import os
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

# Low-pass filter function
def butter_lowpass_filter(data, cutoff, fs, order):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Function to load files with "10" in the name and "_pos_global.sto" for position
def load_files(sample_directory):
    marker_data_path = os.path.join(sample_directory, 'MarkerData')
    opensim_data_path = os.path.join(sample_directory, 'OpenSimData', 'Model')

    if not os.path.exists(marker_data_path) or not os.path.exists(opensim_data_path):
        return None, None, None

    position_file, angle_file, marker_file = None, None, None

    for file_name in os.listdir(opensim_data_path):
        if file_name.endswith('_pos_global.sto') and '10' in file_name:
            position_file = file_name
        if file_name.endswith('_q.sto') and '10' in file_name:
            angle_file = file_name

    for file_name in os.listdir(marker_data_path):
        if file_name.endswith('.trc') and '10' in file_name:
            marker_file = file_name

    if position_file and angle_file and marker_file:
        data_position = process_file_to_dataframe(os.path.join(opensim_data_path, position_file), 19)
        data_angles = process_file_to_dataframe(os.path.join(opensim_data_path, angle_file), 11)
        data_marker = process_file_to_dataframe(os.path.join(marker_data_path, marker_file), 6)
        return data_position, data_angles, data_marker

    return None, None, None

# Function to process files and return DataFrame
def process_file_to_dataframe(file_path, skipped_lines):
    with open(file_path, 'r') as file:
        lines = file.readlines()[skipped_lines:]
    data = [line.strip().split() for line in lines]
    return pd.DataFrame(data)

# Load sample files
data_position, data_angles, data_marker = load_files(Input)

if data_position is not None and data_angles is not None and data_marker is not None:
    # Convert to numpy arrays and filter
    Data_Marker = np.array(data_marker).astype(float)
    Data_Position = np.array(data_position).astype(float)
    Data_Angle = np.array(data_angles).astype(float)

    Time = Data_Position[:, 0]
    fsample = 1 / (Time[2] - Time[1])

    # Filter data
    Data_Marker = np.array([butter_lowpass_filter(Data_Marker[:, col], cutoff, fsample, order) for col in range(Data_Marker.shape[1])]).T
    Data_Position = np.array([butter_lowpass_filter(Data_Position[:, col], cutoff, fsample, order) for col in range(Data_Position.shape[1])]).T
    Data_Angle = np.array([butter_lowpass_filter(Data_Angle[:, col], cutoff, fsample, order) for col in range(Data_Angle.shape[1])]).T

    # Define necessary variables
    Pelvis_X = Data_Position[:, 1]
    Pelvis_Y = Data_Position[:, 2]
    R_Hip_Flexion = Data_Angle[:, 7]
    R_Knee_Flexion = Data_Angle[:, 10]
    L_Hip_Flexion = Data_Angle[:, 15]
    L_Knee_Flexion = Data_Angle[:, 18]
    R_Calc_X = Data_Marker[:, 92]
    L_Calc_X = Data_Marker[:, 110]
    Midhip_X = Data_Marker[:, 23]

    # Kinematic touch-down (TD) and take-off (TO) determination
    R_HeelSacrum = R_Calc_X - Midhip_X
    L_HeelSacrum = L_Calc_X - Midhip_X

    TD_R, _ = find_peaks(R_HeelSacrum, distance=30)
    TD_L, _ = find_peaks(L_HeelSacrum, distance=30)

    # Define angles at TD
    R_Knee_Flexion_TD = [R_Knee_Flexion[TD_R[k]] for k in range(len(TD_R) - 1)]
    R_Hip_Flexion_TD = [R_Hip_Flexion[TD_R[k]] for k in range(len(TD_R) - 1)]
    L_Knee_Flexion_TD = [L_Knee_Flexion[TD_L[k]] for k in range(len(TD_L) - 1)]
    L_Hip_Flexion_TD = [L_Hip_Flexion[TD_L[k]] for k in range(len(TD_L) - 1)]
    
    # Foot position relative to pelvis at TD
    Foot_Position_R_TD = [R_Calc_X[TD_R[k]] - Pelvis_X[TD_R[k]] for k in range(len(TD_R) - 1)]
    Foot_Position_L_TD = [L_Calc_X[TD_L[k]] - Pelvis_X[TD_L[k]] for k in range(len(TD_L) - 1)]

    # Calculate the mean foot position at TD for classification
    Foot_Position_Mean_TD = (np.mean(Foot_Position_R_TD) + np.mean(Foot_Position_L_TD)) / 2

    # Calculate mean values
    R_Knee_Flexion_TD_Mean = np.mean(R_Knee_Flexion_TD)
    R_Hip_Flexion_TD_Mean = np.mean(R_Hip_Flexion_TD)
    L_Knee_Flexion_TD_Mean = np.mean(L_Knee_Flexion_TD)
    L_Hip_Flexion_TD_Mean = np.mean(L_Hip_Flexion_TD)

    Knee_Flexion_TD_Mean_Average = (R_Knee_Flexion_TD_Mean + L_Knee_Flexion_TD_Mean) / 2
    Hip_Flexion_TD_Mean_Average = (R_Hip_Flexion_TD_Mean + L_Hip_Flexion_TD_Mean) / 2
   

    # Athlete classification
    def classify_athlete(Foot_Position_Mean_TD, Hip_Flexion_TD_Mean_Average, Knee_Flexion_TD_Mean_Average):
        if Hip_Flexion_TD_Mean_Average < 31.2:
            if Foot_Position_Mean_TD < 0.126:
                return "Terrestrial"
            else:
                return "Aerial"
        else:
            if Knee_Flexion_TD_Mean_Average < 20.6:
                return "Terrestrial"
            else:
                return "Aerial"

    # Classify the athlete based on mean values
    classification = classify_athlete(Foot_Position_Mean_TD, Hip_Flexion_TD_Mean_Average, Knee_Flexion_TD_Mean_Average)
    print(f"The athlete's classification is: {classification}")
else:
    print("Error loading data.")
