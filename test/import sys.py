import sys
import serial
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import QTimer, Qt

class HeatmapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 960, 720)  # Increase window size
        self.image = QImage(960, 720, QImage.Format_RGB888)  # Adjust heatmap size
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_heatmap)
        self.timer.start(125)  # Update interval in milliseconds
        
        self.temps = np.zeros((24, 32))
        self.serial_port = 'COM21'
        self.baud_rate = 115200
        self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        self.ser.flush()

    def read_serial_data(self):
        if self.ser.in_waiting > 5000:
            line = self.ser.read_until(b"*")
            split_string = line.decode().strip().split(',')

            for q in range(768):
                try:
                    value = float(split_string[q])
                    self.temps.flat[q] = value
                except (ValueError, IndexError):
                    self.temps.flat[q] = 0

    def update_heatmap(self):
        self.read_serial_data()
        self.image.fill(Qt.black)
        painter = QPainter(self.image)
        for i in range(24):
            for j in range(32):
                value = self.temps[i, j]
                color = self.map_value_to_color(value)
                painter.setPen(color)
                painter.drawPoint(j, i)
        self.update()

    def map_value_to_color(self, value):
        if value < 20:
            return Qt.blue
        elif value < 25:
            return Qt.green
        elif value < 30:
            return Qt.yellow
        else:
            return Qt.red

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap.fromImage(self.image)
        painter.drawPixmap(0, 0, pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heatmap Display")
        self.setGeometry(100, 100, 640, 480)
        self.heatmap_widget = HeatmapWidget()
        self.setCentralWidget(self.heatmap_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())