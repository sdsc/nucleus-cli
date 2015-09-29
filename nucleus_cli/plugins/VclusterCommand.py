from __future__ import print_function

import requests
from cloudmesh_base.hostlist import Parameter
from cloudmesh_cmd3light.command import command, Cmd3Command

rest_version = "v1"
base_url = "http://127.0.0.1:8000/" + rest_version + "/"


class VclusterCommand(Cmd3Command):
    topics = {"cluster": "comet"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command cluster")

    def _url(endpoint):
        return base_url + endpoint

    @command
    def do_cluster(self, args, arguments):
        """
        ::

           Usage:
              vcluster info [--user=USER]
                            [--project=PROJECT]
              vcluster list [--name=NAMES]
                            [--user=USER]
                            [--project=PROJECT]
                            [--hosts=HOSTS]
                            [--start=TIME_START]
                            [--end=TIME_END]
                            [--hosts=HOSTS]
                            [--format=FORMAT]
                            [ID]
              vcluster start IDS
              vcluster stop IDS
              vcluster power (on|off) CLUSTERID COMPUTEIDS
              vcluster delete [all]
                              [--user=USER]
                              [--project=PROJECT]
                              [--name=NAMES]
                              [--hosts=HOSTS]
                              [--start=TIME_START]
                              [--end=TIME_END]
                              [--host=HOST]
              vcluster delete --file=FILE
              vcluster update [--name=NAMES]
                              [--hosts=HOSTS]
                              [--start=TIME_START]
                              [--end=TIME_END]
              vcluster add [--user=USER]
                           [--project=PROJECT]
                           [--host=HOST]
                           [--description=DESCRIPTION]
                           [--start=TIME_START]
                           [--end=TIME_END]
                           NAME
              vcluster add --file=FILE

              Options:
                --user=USER           user name
                --name=NAMES          Names of the vcluster
                --start=TIME_START    Start time of the vcluster, in
                                      YYYY/MM/DD HH:MM:SS format.
                                      [default: 1901-01-01]
                --end=TIME_END  End time of the vcluster, in YYYY/MM/DD
                                HH:MM:SS format. In addition a duratio can be
                                specified if the + sign is the first sig The
                                duration will than be added to the start
                                time. [default: 2100-12-31]
                --project=PROJECT     project id
                --host=HOST           host name
                --description=DESCRIPTION  description summary of the vcluster
                --file=FILE           Adding multiple vclusters from one file
                --format=FORMAT       Format is either table, json, yaml or csv
                                      [default: table]
           Description:
               vcluster info
                  lists the resources that support vcluster for
                  a given user or project.

        """

        print(arguments)

        if arguments["list"]:

            id = arguments["ID"]

            if id is None:
                r = requests.get(self._url("cluster"))
            else:
                r = requests.get(self._url("cluster/" + id))
            print(r.status_code)
            print(r.text)

        elif arguments["start"]:

            ids = arguments["IDS"]
            print("start", ids)

        elif arguments["stop"]:

            ids = arguments["IDS"]
            print("stop", ids)

        elif arguments["power"]:

            clusterid = arguments["CLUSTERID"]
            computeids = Parameter.expand(arguments["COMPUTEIDS"])

            if arguments["on"]:

                print("power on")

            elif arguments["off"]:

                print("power off")

            print(clusterid)
            print(computeids)


if __name__ == "__main__":
    main()
