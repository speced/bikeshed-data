#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import bikeshed
import os
import subprocess

def main():
	scriptPath = os.path.dirname(os.path.realpath(__file__))
	dataPath = os.path.join(scriptPath, "data")
	bikeshed.config.quiet = False
	bikeshed.update.update(path=dataPath)
	bikeshed.update.createManifest(path=dataPath)
	os.chdir(scriptPath)
	subprocess.check_call("git add data", shell=True)
	subprocess.check_call("git commit -m 'update data'", shell=True)
	subprocess.check_call("git push", shell=True)

if __name__ == "__main__":
	main()
