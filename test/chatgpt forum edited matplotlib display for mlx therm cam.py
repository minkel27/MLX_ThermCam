import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Serial port configuration
serial_port = 'COM21'
baud_rate = 115200

# Initialize serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)
ser.flush()

# Initialize temperature array
temps = np.zeros(768)

# Create a custom colormap
colors = [(1, 1, 0), (1, 0.5, 0), (1, 0, 0), (0, 0, 0)]  # Yellow, Orange, Red, Black
nodes = [0.0, 0.1, 0.2, 1.0]  

# Create a colormap object
custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", list(zip(nodes, colors)))

# Create the figure for plotting
fig, ax = plt.subplots()
heatmap = ax.imshow(np.zeros((24, 32)), cmap=custom_cmap, vmin=20, vmax=35)
plt.colorbar(heatmap)

# Draw the canvas once so we can cache the background
fig.canvas.draw()

# Cache the background (static elements of the plot)
ax_background = fig.canvas.copy_from_bbox(ax.bbox)

def read_serial_data():
    if ser.in_waiting > 5000:
        line = ser.read_until("*")
        split_string = line.decode().strip().split(',')

        for q in range(768):
            try:
                value = float(split_string[q])
                temps[q] = value
            except (ValueError, IndexError):
                temps[q] = 0
        print(temps)  # Optional: for debugging

def update_heatmap():
    read_serial_data()
    
    # Restore the background
    fig.canvas.restore_region(ax_background)
    
    # Update the heatmap with the new data
    heatmap.set_array(temps.reshape((24, 32)))
    
    # Redraw the heatmap only
    ax.draw_artist(heatmap)
    
    # Blit the updated area to the screen
    fig.canvas.blit(ax.bbox)
    
    # Flush events to make sure everything is updated on the screen
    fig.canvas.flush_events()

plt.show(block=False)

while True:
    update_heatmap()