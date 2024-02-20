import sys
import cv2
import numpy as np
import os


MAX_DISTANCE = 0.35
MIN_DISTANCE = 0.21
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
    

LOAD_PATH = "tof/data/test_daten"

def load_buffers():
    timestamp = "2024-01-11_21-21-45"
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

def on_mouse(event, x, y, flags, param):
    global selectRect,followRect
    
    if event == cv2.EVENT_LBUTTONDOWN:
        pass

    elif event == cv2.EVENT_LBUTTONUP:
        selectRect.start_x = x - 4 if x - 4 > 0 else 0
        selectRect.start_y = y - 4 if y - 4 > 0 else 0
        selectRect.end_x = x + 4 if x + 4 < 240 else 240
        selectRect.end_y=  y + 4 if y + 4 < 180 else 180
    else:
        followRect.start_x = x - 4 if x - 4 > 0 else 0
        followRect.start_y = y - 4 if y - 4 > 0 else 0
        followRect.end_x = x + 4 if x + 4 < 240 else 240
        followRect.end_y = y + 4 if y + 4 < 180 else 180
        
def usage(argv0):
    print("Usage: python "+argv0+" [options]")
    print("Available options are:")
    print(" -d        Choose the video to use")


if __name__ == "__main__":
    cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("preview",on_mouse)
    counter = 0

    depth_buf, amplitude_buf = load_buffers()
    #np.set_printoptions(threshold=sys.maxsize)
    print(depth_buf.shape)
    print(depth_buf)

    while True:
            
        depth_buf, amplitude_buf = load_buffers()
        amplitude_buf*=(255/1024)
        amplitude_buf = np.clip(amplitude_buf, 0, 255)
        
        print("select Rect distance:",np.mean(depth_buf[selectRect.start_y:selectRect.end_y,selectRect.start_x:selectRect.end_x]))
        result_image = process_frame(depth_buf,amplitude_buf)
        result_image = cv2.applyColorMap(result_image, cv2.COLORMAP_TURBO)
        cv2.rectangle(result_image,(selectRect.start_x,selectRect.start_y),(selectRect.end_x,selectRect.end_y),(255,255,255), 1)
        cv2.rectangle(result_image,(followRect.start_x,followRect.start_y),(followRect.end_x,followRect.end_y),(128,128,128), 1)

        cv2.imshow("preview",result_image)

        key = cv2.waitKey(1)
        if key == ord("q"):
            
            exit_ = True
            # cam.stop()
            # cam.close()
            sys.exit(0)

