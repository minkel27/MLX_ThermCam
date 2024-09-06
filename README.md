# Overview
### Summary
- Code based around the MLX 90640
- Possible usages include visualizing temps, ensuring ovens reach a set goal, analyzing efficiency of heat generators, checking temperatures.

# HOW TO START
Pre: go to working code and choose "StartHere"
1. ssh into the pi with "ssh pi@name" where you replace the name with the name of the pi or ip address
2. open the virtual enviornment with "source myenv/bin/activate"
3. run the code with "python code.py"
     - For troubleshooting ensure you have all the packages for each specific import based on the code portion you are using

  - PI PICO: Code.py.py and importcv
    ---
    - Pico captures and sends arrays to your computer via serial communication (code.py.py)
    - importcv dispalys it on your computer
  - PI Zero:
      ---
    - Same but displays in its terminal and was in progress to livestream the image to a flask website 

Getframe error seems to actually be from the buffersize from one of the pixels having an error and rewriting, try increasing the buffer if this persist.


Valuable links/tutorials/different paths
- [PThermalCam with PI4+](https://pypi.org/project/pithermalcam/)
- [Pi Server for mlx in C+](https://github.com/Samox1/ESP_Thermal_Camera_WebServer)
- [OpenCV documentation](https://docs.opencv.org/)
- [Tutorial](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640)
- [I2C with Pi Zero](https://maxbotix.com/blogs/blog/setup-raspberry-pi-zero-for-i2c-sensor?srsltid=AfmBOoqUTfzDqjKhgLzmXYsK0Dl4vK7O5eg-BZ37kyQU6nLxgZZl5ZEw)
