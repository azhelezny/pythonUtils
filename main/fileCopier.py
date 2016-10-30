import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from os.path import basename
import argparse
from rest.Cloudera import Cloudera
from ssh.Mover import LocalMover, RemoteMover

parser = argparse.ArgumentParser(description="this application simplify the procedure of files copying in clusters")
parser.add_argument("file", metavar='file name', type=str, help="file to copy")
parser.add_argument("-host", type=str, help="hostname of target")

args = parser.parse_args()

c = Cloudera(args.host)
hosts = c.get_clustered_hosts()
if not os.path.isfile(args.file):
    print "file " + args.file + " doesn't exist"
    exit(-1)
file_name = basename(args.file)

for host in hosts:
    lm = LocalMover(host)
    lm.move(args.file, "~/" + file_name)
    rm = RemoteMover(host)
    rm.move("~/" + file_name, Cloudera.splice_machine_path + "/lib/")
