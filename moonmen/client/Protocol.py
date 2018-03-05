import json

from synchronization.SynchronizationManager import SynchronizationManager

from twisted.internet.error import ConnectionDone
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

class SynchronizationProtocol(Protocol):
	def __init__(self, factory):
		self.factory = factory
		self.fileProcesses = []
		self.contents = {}

	def connectionMade(self):
		modifications = self.factory.fileSystemManager.getDifferencesSinceLastSync();
		message = {
			'type' : 'modifications',
			'modifications' : modifications
		}
		self.transport.write(json.dumps(message).encode())

	def connectionLost(self, reason):
		if reason.check(ConnectionDone):
			SynchronizationManager.synchronize(self.fileProcesses, self.contents, self.factory.fileSystemManager)
			self.factory.fileSystemManager.syncBackupState()
			reactor.stop()

	def dataReceived(self, data):
		response = {
			'type' : 'error',
			'message' : 'unknown error'
		}
		try:
			message = json.loads(data.decode())
			if message['type'] == 'operations':
				response = self.handleModifications(message['operations'], message['files'])
			elif message['type'] == 'data':
				response = self.handleData(message['data'])
			else:
				response = {
					'type' : 'error',
					'messgae' : 'Message type not recognized'
				}
		except json.JSONDecodeError:
			response = {
				'type' : 'error',
				'message' : 'Message format not recognized'
			}
		finally:
			self.transport.write(json.dumps(response).encode())

	def handleModifications(self, operations, files):
		self.fileProcesses = operations
		otherSystemRequiredData = self.factory.fileSystemManager.getFilesData(files)
		response = {
			'type' : 'data',
			'data' : otherSystemRequiredData
		}
		return response

	def handleData(self, data): #needs-attention (maybe will need modifications)
		self.contents = data
		response = {
			'type' : 'end'
		}
		return response
