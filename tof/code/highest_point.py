import sys
import cv2
import numpy as np
import os


# Parameters to scale the OpenCV Colormap
MAX_DISTANCE = 0.23
MIN_DISTANCE = 0.168
RANGE = MAX_DISTANCE - MIN_DISTANCE

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
    

LOAD_PATH = "tof/data/testreihe_1"

def load_buffers():
    timestamp = "2024-01-26_13-43-46"
    try:
        depth_buf = np.load(os.path.join(LOAD_PATH, f"depth_buf_{timestamp}.npy"))
        amplitude_buf = np.load(os.path.join(LOAD_PATH, f"amplitude_buf_{timestamp}.npy"))
        return depth_buf, amplitude_buf
    except FileNotFoundError:
        print("Dateien nicht gefunden. Stellen Sie sicher, dass Sie den richtigen Pfad angegeben haben.")
        return None, None


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
    # Create a window
    cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)

    # Load buffer arrays from file
    depth_buf, amplitude_buf = load_buffers()
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

    # Print minimum value and show result image with the choosen rectangle
    print("select Rect distance:",min_val)
    result_image = process_frame(depth_buf,amplitude_buf)
    result_image = cv2.applyColorMap(result_image, cv2.COLORMAP_TURBO)
    cv2.rectangle(result_image,(selectRect.start_x,selectRect.start_y),(selectRect.end_x,selectRect.end_y),(255,255,255), 1)
    cv2.imshow("preview",result_image)
    #cv2.imshow("preview_amplitude", amplitude_buf.astype(np.uint8))

    while True:

        key = cv2.waitKey(1)
        if key == ord("q"):
            
            exit_ = True
            # cam.stop()
            # cam.close()
            sys.exit(0)
