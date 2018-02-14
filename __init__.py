#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import bikeshed
import io
import json
import os
import subprocess

def main():
	updateAndCommit()

def updateAndCommit():
	scriptPath = os.path.dirname(os.path.realpath(__file__))
	dataPath = os.path.join(scriptPath, "data")

	try:
		with io.open(os.path.join(dataPath, "manifest.txt"), 'r', encoding="utf-8") as fh:
			_,_,oldManifest = fh.read().partition("\n")
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
		return

	os.chdir(scriptPath)
	subprocess.check_call("git add data", shell=True)
	subprocess.check_call("git commit -m 'update data'", shell=True)
	subprocess.check_call("git push", shell=True)

def updateDataFiles(path):
	# First, update the Bikeshed-managed data files
	# (This updates the manifest file automatically.)
	bikeshed.config.quiet = False
	bikeshed.update.update(path=path, force=True)

	# Then the WPT data files, adding the file to Bikeshed's data folder
	updateWptDataFiles(dataPath=path)

	# And now manually update the Bikeshed manifest again.
	bikeshed.update.manifest.createManifest(path=path)

def updateWptDataFiles(dataPath):
	return # no-op for now until WPT is fixed
	scriptPath = os.path.dirname(os.path.realpath(__file__))
	wptPath = os.path.join(scriptPath, "web-platform-tests")

	os.chdir(scriptPath)
	try:
		subprocess.check_call("git submodule update --remote", shell=True)
	except Exception as e:
		print e
		return
	os.chdir(wptPath)
	try:
		subprocess.check_call("wpt manifest", shell=True)
	except Exception as e:
		print e
		return

	paths = []
	with io.open(os.path.join(wptPath, "MANIFEST.json"), 'r', encoding="utf-8") as infile:
		jsonData = json.load(infile)
		for testType, typePaths in jsonData["items"].items():
			if testType in ("support", "reftest_node"):
				# Not tests
				continue
			paths.extend(typePaths.keys())
	with io.open(os.path.join(dataPath, "wpt-tests.txt"), "w", encoding="utf-8") as outfile:
		for path in sorted(paths):
			outfile.write(path + "\n")

if __name__ == "__main__":
	main()
