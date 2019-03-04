#!/usr/bin/env python

import os
import shlex
import subprocess
from datetime import datetime
import wrapper


wrapper_command = "java -jar /Users/ccampbell/Veracode/Source/vosp-api-wrappers-java-19.2.5.6.jar -action uploadandscan -appname verademo-swift -createprofile false -version '{}' -filepath '{}'"


def build_bca():
    archive_file = os.environ["ARCHIVE_PATH"]

    try:
        output = subprocess.check_output(["vcxcodepkg", "--noui", "-a", archive_file])
        print(output)
    except subprocess.CalledProcessError as e:
        print(e.output)
    else:
        output_split = output.rsplit(" Path: ", 1)
        if len(output_split) == 2:
            bca_file = output_split[1][:-1]
            date = datetime.utcnow().strftime("%-d %b %Y %H:%M")
            command = shlex.split(wrapper_command.format(date, bca_file))
            wrapper.run_wrapper(command)


if __name__ == "__main__":
    build_bca()
