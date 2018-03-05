from client.Protocol import SynchronizationProtocol

from twisted.internet.protocol import ClientFactory

class SynchronisationFactory(ClientFactory):
	def __init__(self, fileSystemManager):
		self.fileSystemManager = fileSystemManager

	def buildProtocol(self, addr):
		return SynchronizationProtocol(self)
