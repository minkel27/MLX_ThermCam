import serial

# Configure the serial port (replace 'COMx' with your port name, e.g., '/dev/ttyACM0' on Linux or 'COM3' on Windows)
ser = serial.Serial('COM19', 115200, timeout=1)

print("Waiting for input. Send '1' to receive 'Hello, World!'")

while True:
    # Read one byte of data from the serial port
    if ser.in_waiting > 0:
        data = ser.read(1).decode('utf-8')
        
        # Check if the received data is '1'
        if data == '1':
            # Send "Hello, World!" message
            ser.write(b'Hello, World!\n')
            print("Sent 'Hello, 1!'")