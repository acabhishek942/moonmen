from server.Protocol import SynchronizationProtocol
from twisted.internet.protocol import Factory

class SynchronisationFactory(Factory):

	def __init__(self, fileSystemManager):
		self.fileSystemManager = fileSystemManager

	def buildProtocol(self, addr):
		return SynchronizationProtocol(self)


