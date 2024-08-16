import board
import digitalio
import time
import busio  # Import I2C busio

#Custom library for the MLX
from adafruit_mlx90640 import adafruit_mlx90640

#LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Initialize I2C
i2c = busio.I2C(scl=board.GP15, sda=board.GP14)

# Initialize the MLX90640 sensor
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = [0] * 768 

while True:
    try:
        mlx.get_frame(frame)
    except ValueError:
        # Retry if there's a ValueError
        continue

    # Print out the temperature data
    for h in range(24):
        for w in range(32):
            t = frame[h * 32 + w]
            print(f"{t:0.1f}, ", end="")
        print()
    print()
    time.sleep(1)  # Delay between readings

## simulating GPIO pins
# #The state of pins
# class Micropython_GPIO:
#     def __init__(self, pin_obj: digitalio.DigitalInOut, state = 'OUT'):
#         self.pin = pin_obj
#         self.set_INOUT(state)

#     def set_INOUT(self, state):
#         if state == 'IN':
#             self.pin.direction = digitalio.Direction.INPUT
#         elif state == 'OUT':
#             self.pin.direction = digitalio.Direction.OUTPUT

#     def high(self):
#         self.pin.value = True

#     def low(self):
#         self.pin.value = False
    
#     def value(self):
#         return self.pin.value
    

# def gpio_init(pin_num):
#     circuitpy_gpio = digitalio.DigitalInOut(getattr(board, f'GP{pin_num}'))
#     print(f'circutpy_gpio: {circuitpy_gpio}')
#     return Micropython_GPIO(circuitpy_gpio)

# #%%
# gpio_pins = {
#     pin_num: gpio_init(pin_num)
#     for pin_num in range(29)
#     if not pin_num in [23, 24, 25]
# }

# # initialize gpio to use
# MLX1_SCL = gpio_pins[0]
# MLX1_SDA = gpio_pins[1]

# # configure gpio to use
# MLX1_SCL.set_INOUT('OUT')
# MLX1_SDA.set_INOUT('OUT')