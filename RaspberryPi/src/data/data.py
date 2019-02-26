"""
This Singleton data class provides thread safe getters and setters for shared resources
"""

from __future__ import with_statement
import threading
import Queue as queue
import numpy as np
# pylint: disable=too-many-instance-attributes

class Singleton(type):
    """
    Creates Singleton instances of Data
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Data(object):
    """
    Thread safe getters and setters of shared resources
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.__proximity = 0
        self.__inductive = 0
        self.__image_raw = np.ndarray((128, 160, 3))
        self.__run_system = False

        # FIFO queues are syncronized
        self.__classified_queue = queue.Queue()
        self.__metal_queue = queue.Queue()

        self.__lock_proximity = threading.RLock()
        self.__lock_inductive = threading.RLock()
        self.__lock_image_raw = threading.RLock()
        self.__lock_run_system = threading.RLock()

    def get_proximity(self):
        """
        Return proximity value
        """
        proximity = 0
        with self.__lock_proximity:
            proximity = self.__proximity
        return proximity

    def set_proximity(self, reading):
        """
        Set proximity value
        """
        with self.__lock_proximity:
            self.__proximity = reading

    def get_inductive(self):
        """
        Return inductive sensor value
        """
        inductive_data = 0
        with self.__lock_inductive:
            inductive_data = self.__inductive
        return inductive_data

    def set_inductive(self, reading):
        """
        Set inductive sensor value
        """
        with self.__lock_inductive:
            self.__inductive = reading

    def get_image_raw(self):
        """
        Return image take by Pi
        """
        image = np.ndarray((128, 160, 3))
        with self.__lock_image_raw:
            image = self.__image_raw
        return image

    def set_image_raw(self, image):
        """
        Set image take by Pi
        """
        with self.__lock_image_raw:
            self.__image_raw = image

    def enqueue_metal_queue(self, metallic):
        """
        Enqueues metal (1) or non-metal (0)
        """
        self.__metal_queue.put(metallic)

    def dequeue_metal_queue(self):
        """
        Dequeue and returns 1 or 0 for metallic
        """
        return self.__metal_queue.get()

    def metal_queue_empty(self):
        return self.__metal_queue.empty()

    def enqueue_classified_queue(self, classification):
        """
        Enqueues classification
        """
        self.__classified_queue.put(classification)

    def dequeue_classified_queue(self):
        """
        Dequeue and returns classification
        """
        return self.__classified_queue.get()

    def get_run_system(self):
        """
        Return flag for starting motor system
        """
        run = False
        with self.__lock_run_system:
            run = self.__run_system
        return run

    def set_run_system(self, run):
        """
        Set flag for starting motor system
        """
        with self.__lock_run_system:
            self.__run_system = run
