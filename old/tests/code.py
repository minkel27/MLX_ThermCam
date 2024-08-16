import time
import board
import busio
import adafruit_mlx90640
import serial
import numpy as np
import matplotlib.pyplot as plt

# Initialize I2C and MLX90640 sensor
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
mlx = adafruit_mlx90640.MLX90640(i2c)

ser = serial.Serial('COM21', 115200, timeout=1)
def parse_data(line):
    return [float(x) for x in line.split(", ") if x]

# Initialize plot
plt.ion()  # Interactive mode on
fig, ax = plt.subplots()

# Set up serial communication
uart = board.UART1
uart.baudrate = 115200

# Print MLX90640 serial number
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

# Adjust refresh rate if necessary
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

# Buffer to store frame data
frame = [0] * 768
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        data = parse_data(line)
        
        if len(data) == 32:  # Ensure the line contains the right number of values
            # Convert data to 2D array
            data_array = np.array(data).reshape((24, 32))
            ax.clear()
            ax.imshow(data_array, cmap='hot', interpolation='nearest')
            plt.pause(0.1)  # Update the plot every 0.1 seconds
# while True:
#     try:
#         mlx.getFrame(frame)
#     except ValueError:
#         # Handle exceptions by retrying
#         continue

#     # Send frame data over UART
#     for h in range(24):
#         for w in range(32):
#             t = frame[h * 32 + w]
#             uart.write(f"{t:0.1f}, ".encode())
#         uart.write(b"\n")
#     uart.write(b"\n")
    
    
    
    # Optional: Add a delay to avoid flooding the serial port
    time.sleep(0.1)
