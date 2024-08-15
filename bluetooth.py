import time
import board
import busio
import adafruit_mlx90640
import adafruit_ble
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

# Initialize the MLX90640 thermal camera
mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

# Set the refresh rate
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

# Initialize Bluetooth UART service
ble = adafruit_ble.BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

frame = [0] * 768

while True:
    try:
        mlx.getFrame(frame)
    except ValueError:
        continue
    
    # Convert frame data to CSV format for transmission
    frame_data = ",".join([f"{t:.1f}" for t in frame])
    
    # Send data over Bluetooth
    ble.start_advertising(advertisement)
    if uart.connected:
        uart.write(frame_data + "\n")
    ble.stop_advertising()
    
    # Wait for a bit before the next frame
    time.sleep(0.5)