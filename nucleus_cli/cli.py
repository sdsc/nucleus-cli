from __future__ import print_function

from docopt import docopt
from nucleus_cli.version import version
import sys
import requests
from cloudmesh_base.hostlist import Parameter

rest_version = "v1"
base_url = "http://127.0.0.1:8000/" + rest_version + "/"



def main():
    """Usage:
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
          vcluster start ID
          vcluster stop ID
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

    arguments = docopt(main.__doc__, help=True)
    arg = sys.argv[1:]
    print(arguments)
    print(arg)


    def _url(endpoint):
        return base_url + endpoint


    if arguments["list"]:

        id = arguments["ID"]

        if id is None:
            r = requests.get(_url("cluster"))
        else:
            r = requests.get(_url("cluster/" + id))
        print (r.status_code)
        print (r.text)


    elif arguments["start"]:

        id = arguments["ID"]
        print("start", id)

    elif arguments["stop"]:

        id = arguments["ID"]
        print("stop", id)

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

