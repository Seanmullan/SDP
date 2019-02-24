"""
Acts as a fake IO class for Sandbox simulator. Used to test logic flow of program.
Most of the methods have no functionality, they are just there to replace the
methods from the real IO_Tools class, hence the long list of linter disabling.
"""

#pylint: disable=invalid-name
#pylint: disable=no-self-use
#pylint: disable=unused-argument
#pylint: disable=too-few-public-methods
#pylint: disable=wrong-import-position
import sys
sys.path.append('data/')
import threading
import numpy as np
import data

class IOTools(object):
    """
    Initialises fake drivers
    """
    def __init__(self):
        self.camera = Camera()
        self.interface_kit = InterfaceKitHelper()
        self.motor_control = MotorControl()
        self.data = data.Data()

        def read_data():
            """
            Updates fake driver data
            """
            while True:
                proximity = self.data.get_proximity()
                inductive = self.data.get_inductive()
                sensor_data = np.array([proximity, inductive, 0, 0, 0, 0, 0, 0])
                self.interface_kit.setSensors(sensor_data)

        self.thread_read_data = threading.Thread(target=read_data)
        self.thread_read_data.start()


class Camera(object):
    """
    Fake Camera object
    """
    def __init__(self):
        pass

    def initCamera(self, camera='pi', resolution='low'):
        """
        Return fake Camera object
        """
        return self

    def getFrame(self):
        """
        Return dummy image
        """
        return np.zeros(500)

    def imshow(self, name, image):
        """
        Dummy function for image display
        """
        pass

class InterfaceKitHelper(object):
    """
    Fake sensor driver class
    """

    def __init__(self):
        self.__inputs = np.zeros(8)
        self.__sensors = np.array([15, 1000, 0, 0, 0, 0, 0, 0])

    def getInputs(self):
        """
        Return dummy readings
        """
        return self.__inputs[:]

    def getSensors(self):
        """
        Return dummy readings
        """
        return self.__sensors[:]

    def setSensors(self, sensor_data):
        """
        Sets dummy sensor data
        """
        self.__sensors = sensor_data

class MotorControl(object):
    """
    Fake motor driver class
    """
    def __init__(self):
        pass

    def setMotor(self, motor_id, speed):
        """
        Set dummy motors
        """
        pass

    def stopMotor(self, motor_id):
        """
        Set dummy motor by id
        """
        pass

    def stopMotors(self):
        """
        Set all dummy motors
        """
        pass

    def __write(self, value):
        """
        Write to dummy motor
        """
        pass
