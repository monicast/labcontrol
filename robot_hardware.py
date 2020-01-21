"""Provide low level control of robot
This should be considered a sort of simulation 
of a robot
"""

import random
import threading
import os
import time

class robot_hw:
    """ 
    """
    def __init__(self, output):
        """Initialize robot with default settings
        """
        self.position = [random.randrange(0, 3000), random.randrange(0, 3000), random.randrange(0, 3000)]
        self._velocity = 1
        self._acceleration = 1
        self._status = 'on'
        self._output = output
        self.__op_thread = threading.Thread(target = self.__show_start_robot)
        self.__op_thread.start()
    
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        self._velocity = value
        output = open(self._output, 'a');
        output.write(f'\nSetting velocity to {value}')
        output.close()
    
    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = value
        output = open(self._output, 'a');
        output.write(f'\nSetting acceleration to {value}')
        output.close()
        

    def move(self, goal_position):
        """Move the robot
        Return True for successful move, False for failure
        """
        if not self.ready_for_new_action():
            print('Robot busy')
            return False
        if self._status == 'off':
            print('Robot is shutdown. Cannot move')
            return False
        if (goal_position[0] == self.position[0]) and (goal_position[1] == self.position[1]) and (goal_position[2] == self.position[2]):
            output_file_handle = open(self._output, 'a')
            output_file_handle.write(f'\nAlready at {goal_position}')
            output_file_handle.flush()
            output_file_handle.close()
            return True
        else:
            self.__op_thread = threading.Thread(target=self.__show_move, args=(self.position, goal_position))
            self.__op_thread.start()
            self.position = goal_position
            return True
    
    def __show_move(self, start_pos, finish_pos):
        output_file_handle = open(self._output, 'a')
        output_file_handle.write(f'\nMoving robot from {start_pos} to {finish_pos}\n')
        for cnt in reversed(range(random.randint(5,15))):
            output_file_handle = open(self._output, 'a')
            time.sleep(1)
            output_file_handle.write(str(cnt) + '...')
            output_file_handle.close()
        output_file_handle = open(self._output, 'a')
        output_file_handle.write('\nMovement complete')
        output_file_handle.write(f'\nCurrent postion: {self.position}')
        output_file_handle.close()


    def __show_start_robot(self):
        output_file_handle = open(self._output, 'a')
        output_file_handle.write('\nRobot starting up\n')
        output_file_handle.close
        for cnt in reversed(range(1,random.randint(5,15))):
            output_file_handle = open(self._output, 'a')
            time.sleep(1)
            output_file_handle.write(str(cnt) + '...')
            output_file_handle.close()
        output_file_handle = open(self._output, 'a')
        output_file_handle.write('\nRobot ready')
        output_file_handle.close()
    
    def ready_for_new_action(self):
        return not self.__op_thread.is_alive()

    def shutdown(self):
        self._status = 'off'
        output_file_handle = open(self._output, 'a')
        output_file_handle.write('\nShutting down robot')
        output_file_handle.close()




