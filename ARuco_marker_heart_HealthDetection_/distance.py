import cv2 as cv
from cv2 import aruco
import numpy as np
import os
import csv
import time
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
# from arduino_data import *
import serial

# Configure the serial port

# from call import *
calib_data_path = "../calib_data/MultiMatrix.npz"

calib_data = np.load(calib_data_path)
print(calib_data.files)

cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

MARKER_SIZE = 5  # centimeters

marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

param_markers = aruco.DetectorParameters_create()


app = QApplication(sys.argv)
window = QMainWindow()
central_widget = QWidget(window)
window.setCentralWidget(central_widget)
layout = QVBoxLayout()
central_widget.setLayout(layout)

plot_widget = pg.PlotWidget()
layout.addWidget(plot_widget)

x = np.linspace(0, 10, 100)
y = np.sin(x)
curve = plot_widget.plot(x, y)

pen = pg.mkPen(color='r', width=2, style=pg.QtCore.Qt.DashLine)
curve.setPen(pen)

ls=[]
ls_=[]
ls_1=[]
    

def update_plot(x,y):
    # global x, y
    # x += 0.1
    # y = np.sin(x)
    for i in range(100):
        ls_.append(x)
        ls_1.append(y)
    x=ls_
    y=ls_1
    # print(x,y)
    curve.setData(x,y)


def run_prg(*args):
    [ls.append(i.split(",")) for i in args]
    # os.mkdir(ls[0][0])
    count=0
    state=True
    
    
    folder_name = str(ls[0][0])  # Replace with the folder name you created
    filename = str(ls[0][0] + ".avi")
    output_frame_rate = 30
    cap = cv.VideoCapture(0)

    # Get the video frame width and height
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Step 2: Create the video writer

    fourcc = cv.VideoWriter_fourcc(*'XVID')  # Video codec, e.g., 'XVID' for .avi format
    fldr=str(os.makedirs(str("{}".format(folder_name))))
    base_dir = str(os.path.abspath(folder_name))
    out = cv.VideoWriter(os.path.join(base_dir,filename), fourcc, output_frame_rate, (frame_width, frame_height))

    # out = cv.VideoWriter(os.path.join(base_dir,"DFsdfsf.avi"),fourcc, 20,(320,180),False)
    csv_path=os.path.join(base_dir, (str(ls[0][1] + ".csv")))
    header=['time','breath_distance','breath_count','status']
    file_=open(csv_path,'w',newline='')
    writer = csv.writer(file_)
    writer.writerow(header)
    lst=[]
    while True:
        
        heart_status=None
        ret, frame = cap.read()

        if not ret:
            break
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        marker_corners, marker_IDs, reject = aruco.detectMarkers(
            gray_frame, marker_dict, parameters=param_markers
        )
        # result.write(frame)
        
        if marker_corners:
            rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
                marker_corners, MARKER_SIZE, cam_mat, dist_coef
            )
            total_markers = range(0, marker_IDs.size)
            for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
                cv.polylines(
                    frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
                )
                corners = corners.reshape(4, 2)
                corners = corners.astype(int)
                top_right = corners[0].ravel()
                top_left = corners[1].ravel()
                bottom_right = corners[2].ravel()
                bottom_left = corners[3].ravel()


                # Calculating the distance
                distance = np.sqrt(
                    tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
                )
                distance=(distance + 12)
                current_time_seconds = time.time()
                
                # Convert seconds to milliseconds (1 second = 1000 milliseconds).
                current_time_milliseconds = int(current_time_seconds * 1000)
                time_=(str(current_time_milliseconds))

                point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
                cv.putText(
                    frame,
                    f"id: {ids[0]} Dist: {round(distance, 2)}",
                    top_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1.3,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
                cv.putText(
                    frame,
                    f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                    bottom_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1.0,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
                # count=0
                if (distance>42):
                    count=count
                    if (state ==True):
                        count =count + 1
                        if current_time_seconds >=10:
                            if count<8:
                                heart_status = "weak"
                            else:
                                heart_status = "normal"
                                
                        
                        cv.putText(
                            frame,
                            f"Dist: {round(count, 2)}",
                            (30, 40),
                            cv.FONT_HERSHEY_PLAIN,
                            1.4,
                            (0, 255, 0),
                            2,
                            cv.LINE_AA,
                        )
                        state=False
                else:
                    state=True
                    count=count
                    cv.putText(
                        frame,
                        f"Dist: {round(count, 2)}",
                        (30, 40),
                        cv.FONT_HERSHEY_PLAIN,
                        1.4,
                        (0, 255, 0),
                        2,
                        cv.LINE_AA,
                    )
            
                update_plot(current_time_seconds,distance)
               
                vale = [current_time_seconds,distance,count,heart_status]
                writer.writerow(i for i in vale) 
                # print(ids, "  ", corners)
       
        cv.imshow("frame", frame)
        out.write(frame)

        key = cv.waitKey(1)
        if key == ord("q"):
            file_.close()
            break

    
    cap.release()
    out.release()
    
    # re.release()
    cv.destroyAllWindows()
run_prg(input())

# timer = QTimer()
# timer.timeout.connect(run_prg(input()))
# timer.start(100)  # Update every 100 milliseconds

window.show()
sys.exit(app.exec_())