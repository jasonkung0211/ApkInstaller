#!/usr/bin/python

import subprocess
import os
import sys
import fnmatch


def current_path():
    return os.path.dirname(os.path.abspath(__file__))


def list_apk(path):
    return fnmatch.filter(os.listdir(path), '*.apk')


def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,"no": False, "n": False}
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
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


if __name__ == '__main__':
    for filename in list_apk(current_path()):
        print 'After this operation, the Android application package will be installed:'
        print '  '+filename
        if query_yes_no('Do you want to continue ?', 'yes'):
            subprocess.call("adb install -r " + filename, shell=True)
        else:
            print('\n')

