#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import subprocess
try:
    # Py2
    import ConfigParser as configparser
except ImportError:
    # Py3
    import configparser


def run_wrapper(command):
    creds_file = os.path.join(os.path.expanduser("~"), ".veracode", "credentials")
    config = configparser.ConfigParser()
    config.readfp(open(creds_file))
    vid = config.get("default", "veracode_api_key_id")
    vkey = config.get("default", "veracode_api_key_secret")

    command = command + ["-vid", vid, "-vkey", vkey]

    try:
        subprocess.call(["osascript", "-e", "display notification \"Starting BCA upload\" with title \"Veracode\""])
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        subprocess.call(["osascript", "-e", "display notification \"BCA upload complete\" with title \"Veracode\""])
        print(output)
    except subprocess.CalledProcessError as e:
        subprocess.call(["osascript", "-e", "display notification \"BCA upload error\" with title \"Veracode\""])
        print(e.output)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        command = sys.argv[1:]
        run_wrapper(command)
    else:
        print("This script will add -vid and -vkey to a wrapper command from ~/.veracode/credentials (default section)")
        print("Usage: wrapper.py java -jar /path/to/wrapper.jar -action ...")
    
