import json

from synchronization.SynchronizationManager import SynchronizationManager

from twisted.internet.error import ConnectionDone
from twisted.internet.protocol import Protocol


class SynchronizationProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.fileProcesses = []
        self.contents = {}

    def dataReceived(self, contents):
        response = {
            'type' : 'error',
            'message' : 'Unknown error'

        }
        try:
            message = json.loads(contents.decode())
            if message['type'] == 'modifications':
                response = self.handleModifications(message['modifications'])
                
            elif message['type'] == 'data':
                response = self.handleData(message['data'])
            elif message['type'] == 'end':
                self.transport.loseConnection()
            else:
                response = {
                    'type' : 'error',
                    'message' : 'Message type not recognized'
                }
        except json.JSONDecodeError:
            response = {
                'type' : 'error',
                'message' : 'Message format not recognized'
            }
        finally:
            self.transport.write(json.dumps(response).encode())

    def connectionLost(self, reason):
        if reason.check(ConnectionDone):
            SynchronizationManager.synchronize(self.fileProcesses, self.contents, self.factory.fileSystemManager)
            self.factory.fileSystemManager.syncBackupState()


    def handleModifications(self, otherSystemModifications):
        mySystemModifications = self.factory.fileSystemManager.getDifferencesSinceLastSync()
        self.synchroniser = SynchronizationManager(mySystemModifications, otherSystemModifications)
        mySystemFileProcesses, otherSystemFileProcesses = self.synchroniser.getFileProcesses()
        self.mySystemRequiredFiles = self.synchroniser.getRequiredFiles(mySystemFileProcesses)
        self.otherSystemRequiredFiles = self.synchroniser.getRequiredFiles(otherSystemFileProcesses)
        self.fileProcesses = mySystemFileProcesses


        response = {
            'type' : 'operations', #needs-attention
            'operations': otherSystemFileProcesses,
            'files' : self.otherSystemRequiredFiles
        }


        return response


    def handleData(self, data):
        mySystemData, otherSystemData = self.synchroniser.getData(
            data, self.mySystemRequiredFiles, self.otherSystemRequiredFiles, self.factory.fileSystemManager)
        self.contents = mySystemData
        response = {
            'type' : 'data',
            'data' : otherSystemData
        }
        return response
