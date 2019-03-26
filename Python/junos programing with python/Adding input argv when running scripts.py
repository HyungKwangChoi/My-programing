from __future__ import division 
import sys
import re
import getopt

###############################################################################
#  function to print usage and exit
###############################################################################

def usage():
    print "Usage:"
    print "  Input_argv_test.py -s <slot> -c <chip>"
    print "Madatory Options (s, c):"
    print "  slot                : FPC slot number"
    print "  chip                : Chip number"
    print "Optional Options (l, h) :"
    print "  -h                  : help command\n"
    sys.exit(2)

###############################################################################
# Main function called Script starts here
###############################################################################
def main(slot, chip):
    print "program starts here after receiving argv"

#  issue_commands(slot, chip)
#  process_results(slot, chip)

###############################################################################
# Running when the script starts
###############################################################################


if __name__ == "__main__":
    print "Test for input argv when executing the commands"
    print "please follow basis formats"
    print "---------------------------------------------------------------\n"

    print len(sys.argv)   
    if ((len(sys.argv) < 2) or (len(sys.argv) > 2 and len(sys.argv)< 5)):      
        print "ERROR :: Not enough arguments provided. Please check usage below\n"
        usage()

             
    # Parse the arguments
    try:       
        opts,args = getopt.getopt(sys.argv[1:],"s:c:h",[])
    except getopt.GetoptError:   
        print "ERROR :: Seems to be an error with input arguments. Please check usage below\n"
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-s"):
            slot = int(arg)
        elif opt in ("-c"):
            chip = int(arg)
  

    try:
        slot
        chip

    except:
        usage()
    # Start executing
    main(slot, chip)