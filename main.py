#!/usr/bin/python

import fnmatch
import os
import subprocess
import sys

from colorama import Fore, Style
from AndroidDevice import AndroidDevice


def current_path(file):
    return os.path.dirname(os.path.abspath(file))


def list_apk(path):
    return fnmatch.filter(os.listdir(current_path(path)), '*.apk')


def run_camd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()


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


def scan_devices():
    clients_list = []
    substring = "unauthorized"
    returnee, out, err = run_camd("adb devices -l")
    if returnee != 0:
        print("bitcoin failed %d %s %s" % (returnee, out, err))
        exit(returnee)

    for line in out.splitlines()[1:]:
        if not line.strip():
            continue

        serial = line[0:str(line).index(" ")]

        if substring in line:
            clients_list.append(AndroidDevice(serial))
        else:
            product = line[str(line).index("t:"):]
            product = product[2:str(product).index(" ")]
            model = line[str(line).index("l:"):]
            model = model[2:str(model).index(" ")]
            device = line[str(line).index("e:"):]
            device = device[2:str(device).index(" ")]
            port_id = line[str(line).index("d:"):]
            port_id = port_id[2:]
            clients_list.append(AndroidDevice(serial, product, model, device, port_id))

    return clients_list


def print_result(results_list):
    print(" id\t\tproduct\t\tmodel\t\tdevice\t\t\ttransport_id")
    print("-" * 60)
    for count, device in enumerate(results_list, start=1):
        device.print(count)


if __name__ == '__main__':
    devices = scan_devices()
    if len(devices) > 0:
        print_result(devices)
    else:
        print("ADB No Devices Found")
        exit(-1)

    apks = []
    if len(sys.argv) > 1:
        for root, dirs, files in os.walk(sys.argv[1]):
            for filename in fnmatch.filter(files, '*.apk'):
                apks.append(os.path.join(root, filename))
    else:
        if getattr(sys, 'frozen', False):
            apks = list_apk(sys.executable)
        else:
            apks = list_apk(__file__)

    if len(apks) <= 0:
        print("No APK Found")
        exit(-1)

    try:
        choice_target = int(input(
            '\nWhich one device would y to upgrade? upgrade all please type zero(' + Fore.RED + '0' + Style.RESET_ALL + '):').lower())
    except ValueError:
        exit(-1)

    for filename in apks:
        print(
            Fore.BLUE + 'After this operation, the Android application package will be installed:' + ' ' + Fore.GREEN + filename + Style.RESET_ALL)
        if query_yes_no('Do you want to continue ?', 'yes'):
            if choice_target != 0:
                ret, out, err = run_camd("adb -s " + devices[choice_target - 1].serial + " install -r " + filename)
                if ret != 0:
                    print("bitcoin failed %d %s %s" % (ret, out, err))
                    exit(ret)
                print(out)
            else:
                for dev in devices:
                    ret, out, err = run_camd("adb -s " + dev.serial + " install -r " + filename)
                    if ret != 0:
                        print("bitcoin failed %d %s %s" % (ret, out, err))
                        exit(ret)
                    print(out)
        else:
            print('\n')
