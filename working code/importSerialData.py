import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# Serial port configuration
serial_port = 'COM21'
baud_rate = 115200

# Initialize serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)
ser.flush()

# Initialize temperature array
line:str = ""
temps = np.zeros(768)
temp_max = 200
temp_min = 0

# Create a custom colormap
colors = [(1, 1, 0), (1, 0.5, 0), (1, 0, 0), (0, 0, 0)]  # Yellow, Orange, Red, Black
nodes = [0.0, 0.1, 0.2, 1.0]  

# Create a colormap object
custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", list(zip(nodes, colors)))

# Create the figure for plotting
fig, ax = plt.subplots()
heatmap = ax.imshow(np.zeros((24, 32)), cmap=custom_cmap, vmin=20, vmax=35)
plt.colorbar(heatmap)

def read_serial_data():
    if ser.in_waiting > 5000:
        line = ser.read_until("*")
        # if len(line) > 4608:
        #     line = line[:4608]
        split_string = line.decode().strip().split(',')

        for q in range(768):
            try:
                value = float(split_string[q])
                temps[q] = value
            except (ValueError, IndexError):
                temps[q] = 0
        print(line)
    print(temps)

def update_heatmap(*args):
    read_serial_data()
    heatmap.set_array(temps.reshape((24, 32)))
    return heatmap,

ani = animation.FuncAnimation(fig, update_heatmap, interval=62.5)

plt.show()