import argparse

from server.Factory import SynchronisationFactory as ServerFactory
from client.Factory import SynchronisationFactory as ClientFactory
from filesystem.FileSystemManager import FileSystemManager

# twisted imports
from twisted.internet import reactor

def server(args):
    filesystemmanager =  FileSystemManager(args.directory, args.backupDirectory)
    reactor.listenTCP(args.port, ServerFactory(filesystemmanager))
    print ("Listening on port " + str(args.port))
    reactor.run()

def client(args):
    filesystemmanager = FileSystemManager(args.directory, args.backupDirectory)
    reactor.connectTCP(args.host, args.port, ClientFactory(filesystemmanager))
    print ('connecting to host ' + args.host + ' on port ' + str(args.port))
    reactor.run()

def main():
    parser = argparse.ArgumentParser(description='Synchronized folder across multiple devices')
    subparsers = parser.add_subparsers(title='subcommands', dest='system',
                    help='start or connect to a moonmen server')


    clientParser = subparsers.add_parser('client',
                help='Connect to a moonmen server to sync directory')
    clientParser.add_argument(
                '-o','--host', required=True, type=str, help='hostname')
    clientParser.add_argument(
                '-p', '--port', required=True, type=int, help='port')
    clientParser.add_argument(
                '-d', '--directory', type=str,
                help='path of directory to sync', default='.')
    clientParser.add_argument(
                '-b', '--backupDirectory', type=str,
                help='path of backup directory to sync', default='./.moonmenBackup')



    serverParser = subparsers.add_parser('server',
                help='Initialize a moonmen server to sync directory')
    serverParser.add_argument(
                '-p', '--port', required=True, type=int, help='port')
    serverParser.add_argument(
                '-d', '--directory', type=str,
                help='path of directory to sync', default='.')
    serverParser.add_argument(
                '-b', '--backupDirectory', type=str,
                help='path of backup directory to sync', default='./.moonmenBackup')

    args = parser.parse_args()

    if args.system == 'client':
        client(args)
    elif args.system == 'server':
        server(args)
    else:
        parser.error('Argument not recognized. Provide one of ("server", "client")')


if __name__ == '__main__':
    main()
