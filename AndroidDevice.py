import atexit
import logging
import os
import re
import subprocess
from colorama import Fore, Style


class AndroidDevice(object):
    def __init__(self, serial, product=None, model=None, device=None, transport=None):

        self.serial = serial
        self.product = product
        self.model = model
        self.device = device
        self.transport = transport

        self.adb_cmd = ['adb']
        if self.serial is not None:
            self.adb_cmd.extend(['-s', serial])
        if self.product is not None:
            self.adb_cmd.extend(['-p', product])
        self._linesep = None
        self._features = None

    def print(self, count):
        print(Fore.RED + "{:-2d}".format(count) + Style.RESET_ALL + "   {} \t\t\t {} \t {} \t\t\t {}".format(self.product,
                                                                                                      self.model,
                                                                                                      self.device,
                                                                                                      self.transport))
        print(Style.RESET_ALL)
        return
