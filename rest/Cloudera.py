import base64

import requests

from files import Parameters
from ssh.Mover import RemoteCommand


class Cloudera:
    splice_machine_path = Parameters.Settings.splice_dir_cloudera

    def __init__(self, host, protocol="http", port=7180, user="admin", password="admin", api_version="api/v9"):
        self.protocol = protocol
        self.host = host
        self.port = format(port)
        self.user = user
        self.password = password
        self.apiVersion = api_version
        self.headers = {'authorization': "Basic " + base64.b64encode(user + ":" + password)}

    def restart_cluster(self):
        command = RemoteCommand(self.host)
        command.execute(Cloudera.splice_machine_path + "/scripts/restart.sh")

    def flatten_cluster(self):
        command = RemoteCommand(self.host)
        command.execute(Cloudera.splice_machine_path + "/scripts/flatten.sh")

    def get_url(self):
        return self.protocol + "://" + self.host + ":" + self.port + "/" + self.apiVersion

    def get_clustered_hosts(self):
        """:rtype: list"""
        result = []
        response = requests.get(url=self.get_url() + "/hosts", headers=self.headers)
        json = response.json()

        for key, value in json.iteritems():
            for host_name in value:
                h_n = host_name["hostname"]
                result.append(h_n)
                print h_n
        return result
