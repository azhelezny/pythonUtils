import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from rest.Cloudera import Cloudera

parser = argparse.ArgumentParser(description="this application simplify the procedure of cluster restart")
parser.add_argument("-host", type=str, help="hostname of target", required=True)

args = parser.parse_args()

c = Cloudera(args.host)
print c.restart_cluster()