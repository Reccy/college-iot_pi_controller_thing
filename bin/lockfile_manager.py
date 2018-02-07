#!/usr/bin/env python2
import os
import fasteners

class lockfile_manager():
	# Checks for the Pi Controller lockfile.
	# Return True if exists, False if not.
	def lockfile_exists(self, lock_location):
		print "Reading lockfile at", lock_location

		exists = fasteners.InterProcessLock(lock_location).exists()

		if exists:
			print "Lockfile found at", lock_location
			return True
		else:
			print "Lockfile not found at", lock_location
			return False

	# Writes a lockfile
	# Return True, fasteners.InterProcessLock if successful, False, fasteners.InterProcessLock if not.
	def lockfile_write(self, lock_location):
		print "Attempting to write lockfile at", lock_location

		if self.lockfile_exists(lock_location):
			print "Lockfile write failed: lockfile already exists at", lock_location
			return {'success':False}

		print "Writing lockfile at", lock_location

		lock = fasteners.InterProcessLock(lock_location)
		lock_acquired = lock.acquire(blocking = False)

		if lock_acquired:
			print "Lockfile write succeeded at", lock_location
			return {'success':True, 'lockfile':lock}
		else:
			print "Lockfile write failed at", lock_location
			return {'success':False}

	# Removes a lockfile
	# Return True if successful, False if not.
	def lockfile_remove(self, lock_location):
		print "Attempting to remove lockfile at", lock_location

		try:
			os.remove(lock_location)
			print "Lockfile removed at", lock_location
			return True
		except OSError as e:
			print "Failed to remove lockfile at", lock_location
			print "Error: ", e
			return False
