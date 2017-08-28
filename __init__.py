#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import bikeshed
import io
import os
import subprocess

def main():
	scriptPath = os.path.dirname(os.path.realpath(__file__))
	dataPath = os.path.join(scriptPath, "data")
	bikeshed.config.quiet = False
	try:
		with io.open(os.path.join(dataPath, "manifest.txt"), 'r', encoding="utf-8") as fh:
			_,_,oldManifest = fh.read().partition("\n")
	except:
		raise
	bikeshed.update.update(path=dataPath, force=True)
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

if __name__ == "__main__":
	main()
