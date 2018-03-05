"""
This module is used for synchronizing the two copies based on the difference.
This module uses the methods from the L{FileSystemManager} class to perform the required operations
on file(s) or directories to keep tem in sync
"""

class SynchronizationManager():
	def __init__(self, mySystemModififications, otherSystemModifications):
		self.mySystemModififications = mySystemModififications
		self.otherSystemModifications = otherSystemModifications
		self.mySystemMovedSource = []
		self.mySystemMovedDestination = []
		self.otherSystemMovedSource = []
		self.otherSystemMovedDestination = []

		self.preSynchronizationModifications()
		if len(self.otherSystemModifications['files_moved']):
			self.otherSystemMovedSource, self.otherSystemMovedDestination = map(list, zip(*self.otherSystemModifications['files_moved']))
		if len(self.mySystemModififications['files_moved']):
			self.mySystemMovedSource, self.mySystemMovedDestination = map(list, zip(*self.mySystemModififications['files_moved']))

	def preSynchronizationModifications(self):
		"""
		Set a couple of dictionary parameters in the 'modifications' dictionary for both my ststem 
		and other system.
		If file(s) are moved then remove the source file(s) from the 'files_modified' list and add
		the destination path to the 'files_created' option of the 'modifications' dictionary
		"""
		mySystemFilesMoved = []
		otherSystemFilesMoved = []

		for movedFileSource, movedFileDestination in self.mySystemModififications['files_moved']:
			if movedFileSource in self.mySystemModififications['files_modified']:
				self.mySystemModififications['files_modified'].remove(movedFileSource)
				self.mySystemModififications['files_created'].append(movedFileDestination)
			else:
				mySystemFilesMoved.append((movedFileSource, movedFileDestination))

		for movedFileSource, movedFileDestination in self.otherSystemModifications['files_moved']:
			if movedFileSource in self.otherSystemModifications['files_modified']:
				self.otherSystemModifications['files_modified'].remove(movedFileSource)
				self.otherSystemModifications['files_created'].append(movedFileDestination)
			else:
				otherSystemFilesMoved.append((movedFileSource, movedFileDestination))

		self.mySystemModififications['files_moved'] = mySystemFilesMoved
		self.otherSystemModifications['files_moved'] = otherSystemFilesMoved

	def getFileProcesses(self):
		"""
		Get the processes performed on the file(s).
		Processes can be either of 'create', 'delete', 'modify' or 'move'
		Serialize the operations performed on both the systems and return the same

		returns : python iterable caontaining all the operations performed on either systems.
		"""
		fileProcesses = []
		fileProcesses.append(self.getDeleteFileProcesses())
		fileProcesses.append(self.getCreateFileProcesses())
		fileProcesses.append(self.getMoveFileProcesses())
		fileProcesses.append(self.getModifyFileProcesses())

		mySystemFileProcesses, otherSystemFileProcesses = [], []
		
		if fileProcesses:
			mySystemFileProcesses, otherSystemFileProcesses = map(list, zip(*fileProcesses))

		serializedMySystemFileProcesses = [process for mySystemProcessList in mySystemFileProcesses for process in mySystemProcessList]
		serializedOtherSystemFileProcesses = [process for otherSystemProcessList in otherSystemFileProcesses for process in otherSystemProcessList]

		return (serializedMySystemFileProcesses, serializedOtherSystemFileProcesses)

	def getDeleteFileProcesses(self):
		"""
		Get the delete operations performed in either systems

		returns : python iterable containing the delete operations on either systems
		"""
		mySystemFileProcesses, otherSystemFileProcesses = [], []

		for deletedFile in self.mySystemModififications['files_deleted']:
			if deletedFile not in (self.otherSystemModifications['files_deleted'] + self.otherSystemModifications['files_modified'] + self.otherSystemModifications['files_created'] + self.otherSystemMovedSource + self.otherSystemMovedDestination):
				otherSystemFileProcesses.append(('delete', deletedFile))

		for deletedFile in self.otherSystemModifications['files_deleted']:
			if deletedFile not in (self.mySystemModififications['files_deleted'] + self.mySystemModififications['files_modified'] + self.mySystemModififications['files_created'] + self.mySystemMovedSource + self.mySystemMovedDestination):
				mySystemFileProcesses.append(('delete', deletedFile))

		return (mySystemFileProcesses, otherSystemFileProcesses)


	def getCreateFileProcesses(self):
		"""
		Get the create operations performed in either systems

		return : python iterable containing the create operations on either systems
		"""
		mySystemFileProcesses, otherSystemFileProcesses = [], []

		for createdFile in self.mySystemModififications['files_created']:
			if createdFile not in self.otherSystemModifications['files_created']:
				otherSystemFileProcesses.append(('create', createdFile))

		for createdFile in self.otherSystemModifications['files_created']:
			if createdFile not in self.mySystemModififications['files_created']:
				mySystemFileProcesses.append(('create', createdFile))



		return (mySystemFileProcesses, otherSystemFileProcesses)


	def getMoveFileProcesses(self):
		"""
		Get the move operations performed in either systems

		return : python iterable containing the move operations on either systems
		"""
		mySystemFileProcesses, otherSystemFileProcesses = [], []

		for movedFileSource, movedFileDestination in self.mySystemModififications['files_moved']:
			if movedFileSource in self.otherSystemModifications['files_modified'] and movedFileDestination in self.otherSystemModifications['files_created']:
				otherSystemFileProcesses.append(('create', movedFileSource)) #needs-attention
				otherSystemFileProcesses.append(('create', movedFileDestination))
			elif movedFileDestination in self.otherSystemModifications['files_created']:
				otherSystemFileProcesses.append(('create', movedFileDestination))
				otherSystemFileProcesses.append(('delete', movedFileSource))
			elif movedFileSource in self.otherSystemModifications['files_deleted']:
				otherSystemFileProcesses.append(('create', movedFileDestination))
			elif movedFileSource in self.otherSystemMovedSource:
				if (movedFileSource, movedFileDestination) in self.otherSystemModifications['files_moved']:
					pass # No process required
				else:
					otherSystemFileProcesses.append(('create', movedFileDestination))

			else:
				otherSystemFileProcesses.append(('move', (movedFileSource, movedFileDestination)))

		for movedFileSource, movedFileDestination in self.otherSystemModifications['files_moved']:
			if movedFileSource in self.mySystemModififications['files_modified'] and movedFileDestination in self.mySystemModififications['files_created']:
				mySystemFileProcesses.append(('create', movedFileSource))
				mySystemFileProcesses.append(('create', movedFileDestination))
			elif movedFileDestination in self.mySystemModififications['files_created']:
				mySystemFileProcesses.append(('create', movedFileDestination))
				mySystemFileProcesses.append(('delete', movedFileSource))
			elif movedFileSource in self.mySystemModififications['files_deleted']:
				mySystemFileProcesses.append(('create', movedFileDestination))
			elif movedFileSource in self.mySystemMovedSource:
				if (movedFileSource, movedFileDestination) in self.mySystemModififications['files_moved']:
					pass # No process required
				else:
					mySystemFileProcesses.append(('create', movedFileDestination))

			else:
				mySystemFileProcesses.append(('move', (movedFileSource, movedFileDestination)))

		return (mySystemFileProcesses, otherSystemFileProcesses)

	def getModifyFileProcesses(self):
		"""
		Get the modify operations performed in either systems

		return : python iterable containing the modify operations on either systems
		"""
		mySystemFileProcesses, otherSystemFileProcesses = [], []

		for modifiedFile in self.mySystemModififications['files_modified']:
			if modifiedFile in self.otherSystemModifications['files_deleted'] or modifiedFile in self.otherSystemMovedSource:
				otherSystemFileProcesses.append(('create', modifiedFile))
			else:
				otherSystemFileProcesses.append(('modify', modifiedFile))

		for modifiedFile in self.otherSystemModifications['files_modified']:
			if modifiedFile in self.mySystemModififications['files_deleted'] or modifiedFile in self.mySystemMovedSource:
				mySystemFileProcesses.append(('create', modifiedFile))
			else:
				mySystemFileProcesses.append(('modify', modifiedFile))

		return (mySystemFileProcesses, otherSystemFileProcesses)


	def getData(self, otherSystemFileData, mySystemRequiredFiles, otherSystemRequiredFiles, filesysytemmanager):
		"""
		Get the contents of the file after performing the 'merge'
		See L{http://www.nmr.mgh.harvard.edu/~you2/dramms/dramms-1.4.3-source/build/bundle/src/BASIS/src/utilities/python/diff3.py}
		for more details on the merge module
		"""
		mySystemData = otherSystemFileData
		otherSystemData = {}

		commonFiles = list(set(mySystemRequiredFiles) & set(otherSystemRequiredFiles))
		for file in commonFiles:
			mySystemFileData = filesysytemmanager.readFile(file)
			backupFileData = filesysytemmanager.readBackupFile(file)
			otherSystemFileData = otherSystemFileData[file]
			mergedFile = merge(mySystemFileData, backupFileData, otherSystemFileData)
			mySystemData[file] = mergedFile
			otherSystemData[file] = mergedFile

		uniqueFiles = list(set(otherSystemRequiredFiles) - set(commonFiles))
		for file in uniqueFiles:
			contents = filesysytemmanager.readFile(file)
			otherSystemData[file] = contents

		return (mySystemData, otherSystemData)




	def getRequiredFiles(self, systemFileProcesses):
		"""
		Get the required files to perform operations on
		"""
		files = []
		for systemFileProcess in systemFileProcesses:
			if systemFileProcess[0] in ('create', 'modify'):
				files.append(systemFileProcess[1])
			elif systemFileProcess[0] == 'move':
				files.append(systemFileProcess[1][1])
		return files

	@staticmethod
	def synchronize(systemFileProcesses, contents, filesystemManager):
		"""
		Get the processes or operations performed in either systems in the form of a dictionary and call
		appropriate filesysytemmanager API to perform the same operations.

		param systemFileProcesses : A python iterable dictionary containing the processes performed on either systems
		param contents : Data to be written on the other system
		param filesystemManager : An instance of an object of L{FileSystemManager}
		"""
		for systemFileProcess in systemFileProcesses:
			if systemFileProcess[0] in ('create', 'modify'):
				filesystemManager.writeFile(systemFileProcess[1], contents[systemFileProcess[1]])
			elif systemFileProcess[0] == 'delete':
				filesystemManager.deleteFile(systemFileProcess[1])
			else:
				filesystemManager.moveFile(systemFileProcess[1][0], systemFileProcess[1][1])









