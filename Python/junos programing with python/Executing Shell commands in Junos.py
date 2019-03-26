from __future__ import division
import sys
import re
import getopt
import subprocess  <==== This used for shell script

#cmd = "cprod -A fpc3 -c "show syslog messages""

lines = []

lines = subprocess.check_output("cprod -A fpc3 -c \"show syslog messages\"", shell=True)  <==== subprocess runs on SHELL..so with the command you can run shell, c, C++ or else on shell
print lines


##check_output used to collect the outputs executed by subprocess