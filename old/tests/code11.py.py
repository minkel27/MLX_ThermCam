#Check serial communications 
print("Starting thermal camera data transmission...")

import time
import board
import busio
import adafruit_mlx90640
import usb_cdc

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

# Initialize the MLX90640 thermal camera
mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

# Set the refresh rate
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

# Create a buffer to hold the frame data
frame = [0] * 768

# Open the USB CDC serial output (this is the default)
serial = usb_cdc.data

while True:
    try:
        # Get the frame data from the MLX90640
        mlx.getFrame(frame)
    except ValueError:
        # If there's a ValueError, just skip this frame
        continue
    
    # Convert the frame data to a string
    frame_data = ",".join([f"{t:.1f}" for t in frame])
    
    # Send the frame data over USB serial
    if serial:
        serial.write((frame_data + "\n").encode())
    
    # Wait a bit before sending the next frame
    time.sleep(0.5)