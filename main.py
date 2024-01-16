#!/usr/bin/python

import subprocess
import os
import sys
import fnmatch
from colorama import Fore, Back, Style
from AndroidDevice import AndroidDevice


def current_path():
    return os.path.dirname(os.path.abspath(__file__))


def list_apk(path):
    return fnmatch.filter(os.listdir(path), '*.apk')


def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def scanDevices():
    clients_list = []
    substring = "unauthorized"
    out = subprocess.check_output("adb devices -l", shell=True).splitlines()
    for line in out[1:]:
        if not line.strip():
            continue

        ids = line[0:str(line).index(" ") - 2]

        if substring in line.decode("UTF-8"):
            clients_list.append(AndroidDevice(ids.decode("utf-8")))
        else:
            product = line[str(line).index("t:"):]
            product = product[:str(product).index(" ") - 2]
            model = line[str(line).index("l:"):]
            model = model[:str(model).index(" ") - 2]
            device = line[str(line).index("e:"):]
            device = device[:str(device).index(" ") - 2]
            port_id = line[str(line).index("d:"):]
            clients_list.append(AndroidDevice(ids.decode("utf-8"), product.decode("utf-8"), model.decode("utf-8"), device.decode("utf-8"), port_id.decode("utf-8")))

    return clients_list


def print_result(results_list):
    print(" id\tdevice product\t\tmodel\t\tdevice\t\t\ttransport_id")
    print("-" * 69)
    for count, device in enumerate(results_list, start=1):
        device.print(count)


if __name__ == '__main__':
    devices = scanDevices()
    print_result(devices)

    try:
        choice_target = int(
            input('\nWhich one device would y to upgrade? upgrade all please type zero(0): ').lower())
    except ValueError:
        exit(0)

    for filename in list_apk(current_path()):
        print(Back.BLUE + 'After this operation, the Android application package will be installed:' + Style.RESET_ALL)
        print('  ' + filename)
        if query_yes_no('Do you want to continue ?', 'yes'):
            if choice_target != 0:
                subprocess.call("adb -s " + devices[choice_target - 1].serial + " install -r " + filename, shell=True)
            else:
                for dev in devices:
                    subprocess.call("adb -s " + dev.serial + " install -r " + filename, shell=True)
        else:
            print('\n')
