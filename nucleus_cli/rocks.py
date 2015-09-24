from docopt import docopt
from nucleus_cli.version import version
class NucleusCli(object):

    @staticmethod
    def cli(arguments):
        print(arguments)
        


def main():
    """Usage:
          rocks add cluster
          rocks list cluster
          rocks remove cluster
          rocks status cluster
          rocks add host vm
          rocks create host vm
          rocks list host vm
          rocks list host nas
          rocks move host vm
          rocks pause host vm
          rocks remove host
          rocks report host vm config
          rocks restore host vm
          rocks save host vm
          rocks set host vm cdrom
          rocks start host vm
          rocks stop host vm
          rocks report host vlan
          rocks sync host vlan
          rocks set host interface
       Description:
           TBD

    """

    arguments = docopt(main.__doc__, help=True)
    arg = sys.argv[1:]
    print(arguments)
    print(arg)

if __name__ == "__main__":
    main()

