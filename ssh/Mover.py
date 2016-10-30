import commands
from subprocess import Popen, STDOUT, PIPE

from files import Parameters


class Mover:
    def __init__(self, host, user="splice", pem_file=Parameters.Settings.pem_file_path):
        self.pemFile = pem_file
        self.user = user
        self.host = host


class RemoteMover(Mover):
    def move(self, source, destination):
        command = "ssh -o \"StrictHostKeyChecking no\" -i " + self.pemFile + " " + self.user + "@" + self.host + \
                  " 'sudo mv " + source + " " + destination + "'"
        print "Remote relocation\n" + command
        return commands.getstatusoutput(command)


class LocalMover(Mover):
    def move(self, source, destination):
        command = "scp -o \"StrictHostKeyChecking no\" -i " + self.pemFile + " " + source + " " + self.user + "@" + self.host + ":" + destination
        print "Copying to remote machine\n" + command
        return commands.getstatusoutput(command)


class RemoteCommand(Mover):
    def execute(self, command):
        executableCommand = "ssh -t -t -o \"StrictHostKeyChecking no\" -i " + self.pemFile + " " + self.user + "@" + self.host + \
                            " '" + command + "'"
        p = Popen(executableCommand, stdout=PIPE,
                  stderr=STDOUT, shell=True)

        while True:
            line = p.stdout.readline()
            print line
            if not line:
                break
        print "DONE"
