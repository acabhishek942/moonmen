from unittest import TestCase
import unittest
from synchronization.SynchronizationManager import SynchronizationManager

# Note : 
# assertCountEqual : Test that sequence first contains the same elements as second, regardless of their order.
# The API for this particular assertion is a little misleading.
# See L{https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertCountEqual} for more details

class SynchronizerTestCases(TestCase):

	def test_fileDeletedOnMyDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": ['deleted_file'],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = []
		expectedOtherSystemFileProcesses = [('delete', 'deleted_file')]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileDeletedOnOtherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": ['deleted_file'],
			"files_modified": [],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [('delete', 'deleted_file')]
		expectedOtherSystemFileProcesses = []
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)

	def test_fileDeletedOnBothDevices(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": ['deleted_file'],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": ['deleted_file'],
			"files_modified": [],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedOtherSystemFileProcesses, expectedMySystemFileProcesses = [], []
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileCreatedOnMyDevice(self):

		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": ['created_file'],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = []
		expectedOtherSystemFileProcesses = [('create', 'created_file')]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses,)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)


	def test_fileCreatedOnOtherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": ['created_file'],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [('create', 'created_file')]
		expectedOtherSystemFileProcesses = []
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileCreatedOnBothDevices(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": ['created_file'],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": ['created_file'],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses, expectedOtherSystemFileProcesses = [], []
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileCreatedOnMyDeviceAndMovedOnOtherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": ['created_file'],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [("moved_file", "created_file")],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [("delete", "moved_file"), ("create", "created_file")]
		expectedOtherSystemFileProcesses = [("create", "created_file")]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileCreatedOnOtherDeviceAndMovedOnMyDevice(self):		
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [("moved_file", "created_file")],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": ['created_file'],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [("create", "created_file")]
		expectedOtherSystemFileProcesses = [("delete", "moved_file"), ("create", "created_file")]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)


	def test_fileCreatedandModifiedOnMyDeviceAndMovedModifiedFileOnAnotherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": ['created_file'],
			"files_deleted": [],
			"files_modified": ['modified_file'],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [('modified_file', 'created_file')],
		}			
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [("create", "modified_file"), ("create", "created_file")]
		expectedOtherSystemFileProcesses = [("create", "modified_file"), ("create", "created_file")]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileCreatedAndModifiedOnOtherDeviceAndMovedOnMyDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [("modified_file", "created_file")],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": ['created_file'],
			"files_deleted": [],
			"files_modified": ['modified_file'],
			"files_moved": [],
		}	
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [("create", "modified_file"), ("create", "created_file")]
		expectedOtherSystemFileProcesses = [("create", "modified_file"), ("create", "created_file")]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)		


	def test_fileModifiedOnMyDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": ['modified_file'],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}		
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses =[]
		expectedOtherSystemFileProcesses = [('modify', 'modified_file')]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)


	def test_fileModifiedOnOtherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": ['modified_file'],
			"files_moved": [],
		}		
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [('modify', 'modified_file')]
		expectedOtherSystemFileProcesses = []
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)	
		
	def test_fileModifiedOnBothDevices(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": ['modified_file'],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": ['modified_file'],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [('modify', 'modified_file')]
		expectedOtherSystemFileProcesses = [('modify', 'modified_file')]	
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileMovedOnMyDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [('moved_file_source', 'moved_file_destination')],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = []
		expectedOtherSystemFileProcesses = [('move', ('moved_file_source', 'moved_file_destination'))]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileMovedOnOtherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [('moved_file_source', 'moved_file_destination')],
		}								
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [('move', ('moved_file_source', 'moved_file_destination'))] 
		expectedOtherSystemFileProcesses = []
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileMovedToSameDestinationOnBothDevices(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [('moved_file_source', 'moved_file_destination')],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [('moved_file_source', 'moved_file_destination')],
		}			
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses, expectedOtherSystemFileProcesses = [], []
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileMovedToDifferentDestinationOnOtherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [('moved_file_source', 'my_moved_file_destination')],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [('moved_file_source', 'other_moved_file_destination')],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [('create', 'other_moved_file_destination')]
		expectedOtherSystemFileProcesses = [('create', 'my_moved_file_destination')]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileDeletedMySystemAndModifiedOnOtherSystem(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": ['modified_file'],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": ['modified_file'],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [('create', 'modified_file')]
		expectedOtherSystemFileProcesses = []
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileModifiedOnMyDeviceAndDeletedOnOtherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": ['modified_file'],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": ['modified_file'],
			"files_modified": [],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = []
		expectedOtherSystemFileProcesses = [('create', 'modified_file')]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)						


	def test_fileDeletedMyDeviceAndMovedOnOtherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": ['moved_file'],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [('moved_file', 'moved_file_destination')],
		}		
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [('create', 'moved_file_destination')]
		expectedOtherSystemFileProcesses = []
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileMovedOnMyDeviceAndDeletedOnOtherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [('moved_file', 'moved_file_destination')],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": ['moved_file'],
			"files_modified": [],
			"files_moved": [],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = []
		expectedOtherSystemFileProcesses = [('create', 'moved_file_destination')]				
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileModifiedAndMovedOnMyDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": ['moved_file'],
			"files_moved": [('moved_file', 'moved_file_destination')],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}		
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = []
		expectedOtherSystemFileProcesses = [('create', 'moved_file_destination')]
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)


	def test_fileModifiedAndMovedOnOtherDevice(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": [],
			"files_moved": [],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": ['moved_file'],
			"files_moved": [('moved_file', 'moved_file_destination')],
		}
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses = [('create', 'moved_file_destination')]
		expectedOtherSystemFileProcesses = []
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)

	def test_fileModifiedAndMovedOnBothDevices(self):
		mySystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": ['moved_file'],
			"files_moved": [('moved_file', 'moved_file_destination')],
		}
		otherSystemModifications = {
			"dirs_created": [],
			"dirs_deleted": [],
			"dirs_modified": [],
			"dirs_moved": [],
			"files_created": [],
			"files_deleted": [],
			"files_modified": ['moved_file'],
			"files_moved": [('moved_file', 'moved_file_destination')],
		}	
		synchronizer = SynchronizationManager(mySystemModifications, otherSystemModifications)
		mySystemFileProcesses, otherSystemFileProcesses = synchronizer.getFileProcesses()
		expectedMySystemFileProcesses, expectedOtherSystemFileProcesses = [], []
		self.assertCountEqual(mySystemFileProcesses, expectedMySystemFileProcesses)
		self.assertCountEqual(otherSystemFileProcesses, expectedOtherSystemFileProcesses)
													
if __name__ == '__main__':
	unittest.main()