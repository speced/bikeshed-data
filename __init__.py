#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import bikeshed
import datetime
import io
import json
import os
import subprocess

def main():
	updateAndCommit()

def updateAndCommit():
	print datetime.datetime.utcnow()

	scriptPath = os.path.dirname(os.path.realpath(__file__))
	dataPath = os.path.join(scriptPath, "data")

	try:
		with io.open(os.path.join(dataPath, "manifest.txt"), 'r', encoding="utf-8") as fh:
			oldDate,_,oldManifest = fh.read().partition("\n")
	except:
		raise

	updateDataFiles(path=dataPath)

	try:
		with io.open(os.path.join(dataPath, "manifest.txt"), 'r', encoding="utf-8") as fh:
			_,_,newManifest = fh.read().partition("\n")
	except:
		raise
	if oldManifest == newManifest:
		# No change
		print "Manifest is unchanged since {0}, nothing to be committed".format(oldDate)
		return

	os.chdir(scriptPath)
	print subprocess.check_output("git add data", shell=True)
	print subprocess.check_output("git commit -m 'update data'", shell=True)
	print subprocess.check_output("git push", shell=True)

def updateDataFiles(path):
	bikeshed.config.quiet = False
	bikeshed.update.update(path=path, force=True)



if __name__ == "__main__":
	main()
