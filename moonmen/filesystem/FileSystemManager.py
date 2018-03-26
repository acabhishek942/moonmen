"""
This module provides API to perform various operations on directory or file(s) based
on the differences between the snapshots of the two directories.
"""
import os
import shutil
import pickle

from os.path import basename, normpath, relpath
from itertools import starmap #needs-attention

from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff

class FileSystemManager():

    def __init__(self, directoryPath, backupDirectoryPath):
        self.directoryPath = directoryPath
        self.backupDirectoryPath = backupDirectoryPath
        self.listdir = lambda path: [
            p for p in os.listdir(path) if p != basename(normpath(backupDirectoryPath))] #needs-attention

    def getDifferencesSinceLastSync(self):
        """
        Get differences between the current directory and backup directory since last sync. 
        """
        oldSnapshot = self.getSnapshotOld()
        currentSnapshot = self.getSnapshotCurrent()
        difference = DirectorySnapshotDiff(oldSnapshot, currentSnapshot)
        return self.getDiffDict(difference)

    def getSnapshotCurrent(self):
        """
        Get the snapshot of the directory in current state.
        See http://pythonhosted.org/pydica-watchdog/_modules/watchdog/utils/dirsnapshot.html for more details
        """
        return DirectorySnapshot(self.directoryPath, listdir=self.listdir)

    def getSnapshotOld(self):
        """
        Get the snapshot of backup directory.
        If backup directory is not present snapshot of current directory
        """
        try:
            with open(''.join((self.backupDirectoryPath, '.snapshot')), 'rb') as snapshotFile:
                snapshot = pickle.load(snapshotFile)
        except FileNotFoundError:
            snapshot = DirectorySnapshot(
                self.directoryPath, listdir=lambda _: []) #needs-attention
        return snapshot

    def getDiffDict(self, difference):
        """
        Get the differences between two snapshots in the form of a dictionary

        param difference: L{watchdog.utils.dirsnapshot.DirectorySnapshotDiff}
        """
        diffDict = {}
        print(difference.__dict__.items())
        for key, value in difference.__dict__.items():
            if key in  ('_dirs_moved', '_files_moved'):
                diffDict[key[1:]] = list(starmap(
                    lambda p1, p2: (relpath(p1, self.directoryPath),
                    relpath(p2, self.directoryPath)), value))
            else:
                diffDict[key[1:]] = list(map(lambda p: relpath(p, self.directoryPath), value))
        print (diffDict)
        return diffDict

    def syncBackupState(self):
        """
        Make or sync the backup directory
        """
        currentSnapshot = self.getSnapshotCurrent()
        try:
            self.deleteDirectory(self.backupDirectoryPath)
        except FileNotFoundError:
            pass
        self.copyDirectory(self.directoryPath, self.backupDirectoryPath)
        with open(''.join((self.backupDirectoryPath, '.snapshot')), 'wb') as snapshotFile:
            pickle.dump(currentSnapshot, snapshotFile)

    def createDirectory(self, path):
        """
        OS command for making directories

        param path : path of the directory to create
        """
        os.makedirs(relpath(self.directoryPath+'/'+path), exist_ok=True)

    def deleteDirectory(self, path):
        """
        Use shutil for deleting directory

        param path : path of the directory to delete
        """
        shutil.rmtree(relpath(path, self.directoryPath))

    def moveDirectory(self, sourcePath, destinationPath):
        """
        Use OS module for moving directory

        param sourcePath: source path of the directory
        param destinationPath : destination path of the directory
        """
        os.renames(relpath(sourcePath, self.directoryPath), relpath(destinationPath, self.directoryPath))

    def copyDirectory(self, sourcePath, destinationPath):
        """
        use shutil.copytree for copying the contents of the directory
        
        param sourcePath: source path of the directory
        param destinationPath : destination path of the directory
        """
        shutil.copytree(relpath(sourcePath, self.directoryPath), relpath(destinationPath, self.directoryPath),
            ignore=lambda *_: [basename(normpath(self.backupDirectoryPath))]) #needs-attention

    def deleteFile(self, path):
        """
        Use OS module to delete file.

        param path : path of file to delete
        """
        os.remove(relpath(path, self.directoryPath))

    def moveFile(self, sourcePath, destinationPath):
        """
        Use OS module to move file(s)

        param sourcePath : source path of the file
        param destinationPath : destination path of the file
        """
        os.renames(relpath(sourcePath, self.directoryPath), relpath(destinationPath, self.directoryPath))

    def readFile(self, path):
        """
        Read the contents of a file 

        paaram path : path of the file to read
        """
        with open(relpath(self.directoryPath+'/'+path), 'r') as readFile:
            return readFile.readlines()

    def writeFile(self, path, data):
        """
        Write the given data to the file

        param data : contents to be written to the file
        param path : path of the file to be written
        """
        with open(relpath(self.directoryPath+'/'+path), 'w') as writeFile:
            writeFile.writelines(data)

    def readBackupFile(self, path):
        """
        Read the contents of the backup file

        param path : path of the backup file
        """
        try:
            return self.readFile(''.join((self.backupDirectoryPath, path)))
        except FileNotFoundError:
            return None

    def getFilesData(self, files):
        """
        Return the data of the file(s) provided in the form of a dictionary

        param files : A python iterable containing the path of the files from which data should be read
        """
        fileDataDictionary = {}
        for file in files:
            try:
                fileDataDictionary[file] = self.readFile(file)
            except FileNotFoundError:
                fileDataDictionary[file] = self.readBackupFile(file)
        return fileDataDictionary