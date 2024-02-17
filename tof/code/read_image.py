import sys
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from scipy.signal import savgol_filter


# Parameters to scale the OpenCV Colormap
MAX_DISTANCE = 0.23
MIN_DISTANCE = 0.168
RANGE = MAX_DISTANCE - MIN_DISTANCE

# Choose the test series
test_series = 'testreihe_1'
# test_series = 'testreihe_2'

# Path to the folder with the buffer files
LOAD_PATH = "tof/data/" + test_series

# Path to the folder where the video and the plot should be saved
SAVE_PATH = "tof/results/" + test_series

os.makedirs(SAVE_PATH, exist_ok=True)
video_path = os.path.join(SAVE_PATH, 'video_' + test_series + '.mp4')
plot_path = os.path.join(SAVE_PATH, 'plot_'+ test_series + '.png')

def process_frame(depth_buf: np.ndarray, amplitude_buf: np.ndarray) -> np.ndarray:
        
    depth_buf = np.nan_to_num(depth_buf)
    amplitude_buf[amplitude_buf<=7] = 0
    amplitude_buf[amplitude_buf>7] = 255

    # Set any value higher or lower than the limits to the limit values (MAX and MIN)
    depth_buf = np.clip(depth_buf, MIN_DISTANCE, MAX_DISTANCE)
    # Scale the values ​​to the selected range
    depth_buf = (1-((depth_buf-MIN_DISTANCE)/RANGE))*255
    # Create result frame
    result_frame = depth_buf.astype(np.uint8)  & amplitude_buf.astype(np.uint8)
    return result_frame 


def load_buffers(timestamp):
    # Load the buffers from the file
    try:
        depth_buf = np.load(os.path.join(LOAD_PATH, f"depth_buf_{timestamp}.npy"))
        amplitude_buf = np.load(os.path.join(LOAD_PATH, f"amplitude_buf_{timestamp}.npy"))
        return depth_buf, amplitude_buf
    except FileNotFoundError:
        print("Dateien nicht gefunden. Stellen Sie sicher, dass Sie den richtigen Pfad angegeben haben.")
        return None, None

def get_timestamps():
    
    # Get all files in the load path
    files = os.listdir(LOAD_PATH)
    depth_files = sorted([f for f in files if f.startswith("depth_buf_") and f.endswith(".npy")])
    amplitude_files = sorted([f for f in files if f.startswith("amplitude_buf_") and f.endswith(".npy")])
    depth_timestamps = [extract_timestamp(f) for f in depth_files]
    amplitude_timestamps = [extract_timestamp(f) for f in amplitude_files]
    timestamps = []

    for timestamp in depth_timestamps:
        if timestamp not in amplitude_timestamps:
            print(f"Keine passende Amplitudenpufferdatei für Tiefenpufferdatei mit Zeitstempel {timestamp} gefunden.")
        else:
            print(f"Es wurde ein Zeitstempel {timestamp} mit zugehörigen Daten gefunden.")
            timestamps.append(timestamp)
    
    return timestamps

def extract_timestamp(filename):
    # Extract the timestamp from the filename
    stripped_name = filename.replace(".npy", "")
    if stripped_name.startswith("depth_buf_"):
        stripped_name = stripped_name.replace("depth_buf_", "")
    elif stripped_name.startswith("amplitude_buf_"):
        stripped_name = stripped_name.replace("amplitude_buf_", "")
    return stripped_name 


class UserRect():
    def __init__(self) -> None:
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

selectRect = UserRect()

followRect = UserRect()
        
# Create a rectangle with the center at (x,y)
def create_rect(x,y,half_rect_length,half_rect_width):
    selectRect.start_x = x - half_rect_length if x - half_rect_length > 0 else 0
    selectRect.start_y = y - half_rect_width if y - half_rect_width > 0 else 0
    selectRect.end_x = x + half_rect_length if x + half_rect_length < 240 else 240
    selectRect.end_y = y + half_rect_width if y + half_rect_width < 180 else 180
    return selectRect.start_x,selectRect.start_y,selectRect.end_x,selectRect.end_y

def usage(argv0):
    print("Usage: python "+argv0+" [options]")
    print("Available options are:")
    print(" -d        Choose the video to use")


if __name__ == "__main__":

    # Create variables
    distance2plant = []
    images = []
    height_of_plant = []

    # Load buffer arrays from file
    timestamps = get_timestamps()

    # Calculate the mean depth of every possible rectangle in the frame
    for timestamp in timestamps:
        depth_buf, amplitude_buf = load_buffers(timestamp)
        amplitude_buf*=(255/1024)
        amplitude_buf = np.clip(amplitude_buf, 0, 255)

        # Define the size of the rectangle in which the mean depth is calculated
        half_rect_length=4
        half_rect_width=4
        
        # Create an array to save the mean values of every possible rectangle in the frame 
        n_rows=int((180-(2*half_rect_length)+1)*(240-(2*half_rect_width)+1))
        result_mean=np.zeros(shape=(n_rows,3))
        i=0

        # Calculate the mean depth of every possible rectangle in the frame
        for y in range(half_rect_length,180-half_rect_length+1):
            for x in range(half_rect_width,240-half_rect_width+1):
                selectRect.start_x,selectRect.start_y,selectRect.end_x,selectRect.end_y=create_rect(x,y,half_rect_length,half_rect_width)
                mean_depth=np.mean(depth_buf[selectRect.start_y:selectRect.end_y,selectRect.start_x:selectRect.end_x])
                result_mean[i]=[x, y, mean_depth]
                i=i+1

        # Find the center of the rectangle with lowest mean value
        min_val=np.nanmin(result_mean, axis=0)[2]
        min_row=np.argwhere(result_mean==min_val)[0][0]
        x_min=int(result_mean[min_row,0])
        y_min=int(result_mean[min_row,1])
        create_rect(x_min,y_min,half_rect_length,half_rect_width)

        # Print minimum value and append result image with the choosen rectangle to the image list
        print("select Rect distance:",min_val)
        distance2plant.append(min_val)
        result_image = process_frame(depth_buf,amplitude_buf)
        result_image = cv2.applyColorMap(result_image, cv2.COLORMAP_TURBO)
        cv2.rectangle(result_image,(selectRect.start_x,selectRect.start_y),(selectRect.end_x,selectRect.end_y),(255,255,255), 1)
        images.append(result_image)

    # Create a video from the images
    height, width, layers = images[0].shape
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 15, (width, height))
    for image in images:
        video.write(image)
    video.release()

    # Plot the height of the plant over time
    plot_timestamps = [datetime.datetime.strptime(t, "%Y-%m-%d_%H-%M-%S") for t in timestamps]
    distance2pot = np.mean(distance2plant[0:11])
    for distance in distance2plant:
        height = distance2pot - distance
        height_of_plant.append(height*1000) 

    # Smooth the curve
    x = np.arange(len(height_of_plant))
    y_smooth = savgol_filter(height_of_plant, 101, 3)

    fig, ax = plt.subplots()
    ax.plot(plot_timestamps, height_of_plant, label='Originaldaten')
    ax.plot(plot_timestamps, y_smooth, 'r-', label='Geglättete Kurve')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    ax.set_xlabel('Zeit')
    ax.set_ylabel('Höhe in mm')
    ax.set_title('Testreihe ' + test_series[-1] + ': Wachstum der Kresse')

    ax.legend()

    plt.savefig(plot_path)
    plt.show()

    sys.exit(0)