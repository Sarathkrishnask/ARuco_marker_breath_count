import serial
import time
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
# Configure the serial port
arduino_port = 'COM7'  # Update this with the correct port
baud_rate = 9600

# Establish the serial connection
ser = serial.Serial(arduino_port, baud_rate)
folder_name = input()
fldr=str(os.makedirs(str("{}".format(folder_name))))
base_dir = str(os.path.abspath(folder_name))

csv_path=os.path.join(base_dir, (str(folder_name + ".csv")))
header=['time','temperature_1','temperature_2']
file_=open(csv_path,'w',newline='')
writer = csv.writer(file_)
writer.writerow(header)



def create_plots():    
    try:
        while True:
            # Read data from the serial port
            current_time_seconds = time.time()
           
            # Convert seconds to milliseconds (1 second = 1000 milliseconds).
            # current_time_milliseconds = int(current_time_seconds * 1000)
            data = (ser.readline().decode().strip()).split(',')
            # print(data)
            vale = [current_time_seconds,data[0],data[1]]
            writer.writerow(i for i in vale) 

    except KeyboardInterrupt:
        ser.close()  # Close the serial connection on Ctrl+C
        data = pd.read_csv(csv_path)  # Replace 'data.csv' with your file's name

        # Step 3: Extract Data
        x = data['time']  
        y = data['voltage_1'] 
        
        y1 = data['voltage_2'] 

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))  # 2 rows, 1 column of subplots

        # Plot on Subplot 1
        ax1.plot(x.values, y1.values,color='b',label='Y1 Data')
        ax1.set_xlabel('X Label')
        ax1.set_ylabel('Y1 Label')
        ax1.yaxis.get_label().set_rotation(0)
        ax1.set_title('Y1 Data Plot')
        ax1.legend()
        ax1.grid()

        # Plot on Subplot 2
        ax2.plot(x.values, y.values,color='r',label='Y2 Data')
        ax2.set_xlabel('X Label')
        ax2.set_ylabel('Y2 Label')
        ax2.yaxis.get_label().set_rotation(0)
        ax2.set_title('Y2 Data Plot')
        ax2.legend()
        ax2.grid()

        # Adjust layout
        plt.tight_layout()

        # Show plots
        plt.show()

if __name__ == "__main__":
    create_plots()
