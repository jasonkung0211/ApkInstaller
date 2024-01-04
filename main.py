#!/usr/bin/python

import subprocess
import os
import sys
import fnmatch
from colorama import Fore, Back, Style


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
    out = subprocess.check_output("adb devices -l", shell=True).splitlines()
    for line in out[1:]:
        if not line.strip():
            continue

        ids = line[0:str(line).index(" ")-2]
        product = line[str(line).index("t:"):]
        product = product[:str(product).index(" ")-2]
        model = line[str(line).index("l:"):]
        model = model[:str(model).index(" ")-2]
        device = line[str(line).index("e:"):]
        device = device[:str(device).index(" ")-2]
        port_id = line[str(line).index("d:"):]
        client_dict = {"id": ids, "device product": product, "model": model, "device": device, "transport_id": port_id}
        clients_list.append(client_dict)

    return clients_list


def print_result(results_list):
    print(" id\tdevice product\t\tmodel\t\tdevice\t\t\ttransport_id")
    print("-" * 69)
    for count, device in enumerate(results_list, start=1):
        print(Fore.RED + "{:-2d}".format(count) + Style.RESET_ALL + "  {}\t\t\t{}\t{}\t\t\t{}".format(
                                              device["device product"],
                                              device["model"],
                                              device["device"],
                                              device["transport_id"]))
    print(Style.RESET_ALL)


if __name__ == '__main__':

    devices = scanDevices()
    print_result(devices)

    try:
        choice_target = int(
            input('\nWhich one device would you choose to upgrade? upgrade all please type zero(0): ').lower())
    except ValueError:
        exit(0)

    if choice_target != 0:
        print(choice_target)
    else:
        print("All")

    for filename in list_apk(current_path()):
        print('After this operation, the Android application package will be installed:')
        print('  ' + filename)
        if query_yes_no('Do you want to continue ?', 'yes'):
            subprocess.call("adb install -r " + filename, shell=True)
        else:
            print('\n')
