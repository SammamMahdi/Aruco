#!/usr/bin/env python3
############## Task1.1 - ArUco Detection ##############

import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import math
import time


def detect_ArUco(img):
    ## function to detect ArUco markers in the image using ArUco library
    ## argument: img is the test image
    ## return: dictionary named Detected_ArUco_markers of the format {ArUco_id_no : corners}, where ArUco_id_no indicates ArUco id and corners indicates the four corner position of the aruco(numpy array)
    ##         for instance, if there is an ArUco(0) in some orientation then, ArUco_list can be like
    ##              {0: array([[315, 163],
    #                           [319, 263],
    #                           [219, 267],
    #                           [215,167]], dtype=float32)}

    Detected_ArUco_markers = {}
    ## enter your code here ##
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    parameters = cv2.aruco.DetectorParameters()
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if corners:
        for ids, corners in zip(ids, corners):
            Detected_ArUco_markers.update({ids[0]: corners})
    return Detected_ArUco_markers


def Calculate_orientation_in_degree(Detected_ArUco_markers):
    ## function to calculate orientation of ArUco with respective to the scale mentioned in problem statement
    ## argument: Detected_ArUco_markers  is the dictionary returned by the function detect_ArUco(img)
    ## return : Dictionary named ArUco_marker_angles in which keys are ArUco ids and the values are angles (angles have to be calculated as mentioned in the problem statement)
    ##          for instance, if there are two ArUco markers with id 1 and 2 with angles 120 and 164 respectively, the
    ##          function should return: {1: 120 , 2: 164}

    ArUco_marker_angles = {}
    ## enter your code here ##
    for key in Detected_ArUco_markers:
        corners = Detected_ArUco_markers[key]
        tl = corners[0][0]  # top left
        tr = corners[0][1]  # top right
        br = corners[0][2]  # bottom right
        bl = corners[0][3]  # bottom left
        top = (tl[0] + tr[0]) / 2, -((tl[1] + tr[1]) / 2)
        centre = (tl[0] + tr[0] + bl[0] + br[0]) / 4, -(
            (tl[1] + tr[1] + bl[1] + br[1]) / 4
        )
        try:
            angle = round(
                math.degrees(np.arctan((top[1] - centre[1]) / (top[0] - centre[0])))
            )
        except:
            # add some conditions for 90 and 270
            if top[1] > centre[1]:
                angle = 90
            elif top[1] < centre[1]:
                angle = 270
        if top[0] >= centre[0] and top[1] < centre[1]:
            angle = 360 + angle
        elif top[0] < centre[0]:
            angle = 180 + angle
        ArUco_marker_angles.update({key: angle})
    return ArUco_marker_angles  ## returning the angles of the ArUco markers in degrees as a dictionary


def calc_theta1(Detected_ArUco_markers):
    if (
        0 in Detected_ArUco_markers
        and 1 in Detected_ArUco_markers
        and 2 in Detected_ArUco_markers
    ):
        corners0 = Detected_ArUco_markers[0]
        tl0 = corners0[0][0]  # top left
        tr0 = corners0[0][1]  # top right
        br0 = corners0[0][2]  # bottom right
        bl0 = corners0[0][3]  # bottom left
        centre0 = (tl0[0] + tr0[0] + bl0[0] + br0[0]) / 4, -(
            (tl0[1] + tr0[1] + bl0[1] + br0[1]) / 4
        )

        corners1 = Detected_ArUco_markers[1]
        tl1 = corners1[0][0]  # top left
        tr1 = corners1[0][1]  # top right
        br1 = corners1[0][2]  # bottom right
        bl1 = corners1[0][3]  # bottom left

        centre1 = (tl1[0] + tr1[0] + bl1[0] + br1[0]) / 4, -(
            (tl1[1] + tr1[1] + bl1[1] + br1[1]) / 4
        )
        corners2 = Detected_ArUco_markers[2]
        tl2 = corners2[0][0]  # top left
        tr2 = corners2[0][1]  # top right
        br2 = corners2[0][2]  # bottom right
        bl2 = corners2[0][3]  # bottom left

        centre2 = (tl2[0] + tr2[0] + bl2[0] + br2[0]) / 4, -(
            (tl2[1] + tr2[1] + bl2[1] + br2[1]) / 4
        )
        l01 = math.sqrt((centre0[1] - centre1[1]) ** 2 + (centre0[0] - centre1[0]) ** 2)
        l02 = math.sqrt((centre0[1] - centre2[1]) ** 2 + (centre0[0] - centre2[0]) ** 2)
        l12 = math.sqrt((centre1[1] - centre2[1]) ** 2 + (centre1[0] - centre2[0]) ** 2)

        angle = math.degrees(
            np.arccos((l01**2 + l02**2 - l12**2) / (2 * l01 * l02))
        )
        # except:
        #     # add some conditions for 90 and 270
        #     if centre0[1] > centre1[1]:
        #         angle = 90
        #     elif centre0[1] < centre0[1]:
        #         angle = 270
        # if centre0[0] >= centre1[0] and centre0[1] < centre1[1]:
        #     angle = 360 + angle
        # elif centre0[0] < centre1[0]:
        #     angle = 180 + angle
        return angle


def mark_ArUco(img, Detected_ArUco_markers, ArUco_marker_angles, theta1):
    ## function to mark ArUco in the test image as per the instructions given in problem statement
    ## arguments: img is the test image
    ##            Detected_ArUco_markers is the dictionary returned by function detect_ArUco(img)
    ##            ArUco_marker_angles is the return value of Calculate_orientation_in_degree(Detected_ArUco_markers)
    ## return: image namely img after marking the aruco as per the instruction given in problem statement

    ## enter your code here ##
    for key in Detected_ArUco_markers:
        corners = Detected_ArUco_markers[key]
        tl = corners[0][0]  # top left
        tr = corners[0][1]  # top right
        br = corners[0][2]  # bottom right
        bl = corners[0][3]  # bottom left
        top = int((tl[0] + tr[0]) // 2), int((tl[1] + tr[1]) // 2)
        centre = int((tl[0] + tr[0] + bl[0] + br[0]) // 4), int(
            (tl[1] + tr[1] + bl[1] + br[1]) // 4
        )
        img = cv2.line(img, top, centre, (255, 0, 0), 3)
        img = cv2.circle(img, (int(tl[0]), int(tl[1])), 6, (100, 100, 100), -1)
        img = cv2.circle(img, (int(tr[0]), int(tr[1])), 6, (0, 255, 0), -1)
        img = cv2.circle(img, (int(br[0]), int(br[1])), 6, (100, 100, 255), -1)
        img = cv2.circle(img, (int(bl[0]), int(bl[1])), 6, (255, 255, 255), -1)
        img = cv2.circle(img, centre, 5, (0, 0, 255), -1)
        img = cv2.putText(
            img,
            str(key),
            centre,
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 200),
            3,
            cv2.LINE_AA,
        )
        img = cv2.putText(
            img,
            f"Theta1: {str(theta1)}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3,
            cv2.LINE_AA,
        )
    return img
