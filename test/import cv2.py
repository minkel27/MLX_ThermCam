import cv2
import time
import serial
import numpy as np

# Serial port configuration
serial_port = 'COM21'
baud_rate = 115200

# Initialize serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)
ser.flush()

# Initialize temperature array
temps = np.zeros((24, 32), dtype=np.float32)

# Color maps and  custom
# Define the colors in BGR format (as OpenCV uses BGR, not RGB)
colors = [
    (0, 0, 0),      # Black
    (0, 0, 255),    # Red
    (0, 127, 255),  # Orange
    (0, 255, 255)   # Yellow
]
colormap = cv2.COLORMAP_HOT  # You can experiment with other OpenCV colormaps
# print(cv2.COLORMAP_JET)

def read_serial_data():
    if ser.in_waiting > 5000:#in bytes
        line = ser.read_until(b"*")
        split_string = line.decode().strip().split(',')

        for q in range(768):
            try:
                value = float(split_string[q])
                if value < 30:
                    value = 30
                temps.flat[q] = value
            except (ValueError, IndexError):
                temps.flat[q] = 0

def update_heatmap():
    read_serial_data()

    # Normalize temps array to the range [0, 255] for OpenCV color mapping
    normalized_temps = cv2.normalize(temps, None, 0, 255, cv2.NORM_MINMAX)

    # Convert to 8-bit unsigned integer format for color mapping
    normalized_temps = np.uint8(normalized_temps)

    # Apply the colormap
    colored_map = cv2.applyColorMap(normalized_temps, colormap)

    # Resize to desired window size
    resized_map = cv2.resize(colored_map, (960, 720), interpolation=cv2.INTER_NEAREST)

    # Display the image
    cv2.imshow(
        'Heatmap Display', 
        resized_map,
        # colored_map
    )

def main():
    
    while True:
        time.sleep(0.1)
        start = time.time()
        # read_serial_data()
        update_heatmap()
        end = time.time()
        # print(f"{temps}")
        print(f"Here is the diff: {end-start}")
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit when 'q' is pressed
            break

    ser.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
