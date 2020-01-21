"""
Providing some higher level control of the robot
"""

import pandas as pd
import json
import robot_hardware

import threading 

class robot:
    def __init__(self, settings_file='', waypoint_file=''):
        """Start the robot with settings. Load a set of waypoints"""
        self.settings_file = settings_file
        self.__robot_interface = robot_hardware.robot_hw('output.txt')
        self.__upload_settings()
        self.waypoints = self.__read_waypoints(waypoint_file)
    
    def __read_waypoints(self, waypoint_file):
        return pd.read_csv(waypoint_file, index_col=0)
    
    def __upload_settings(self):
        with open(self.settings_file) as f:
            settings_data = json.load(f)
        self.__robot_interface._velocity = settings_data['velocity']
        self.__robot_interface._acceleration = settings_data['acceleration']
    
    def move_abs(self, loc):
        if not self.__robot_interface.move(loc):
            print('ERROR: Failed to move robot')

    def move_to_waypoint(self, waypoint_name):
        new_location = self.waypoints.loc[waypoint_name,:].tolist()
        if not self.__robot_interface.move(new_location):
            print('ERROR: Failed to move robot')