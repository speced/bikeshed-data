#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import os
import subprocess

import bikeshed


def main():
    updateAndCommit()


def updateAndCommit():
    print(datetime.datetime.utcnow())
    print(subprocess.check_output("git pull", shell=True).decode(encoding="utf-8"))

    scriptPath = os.path.dirname(os.path.realpath(__file__))
    dataPath = os.path.join(scriptPath, "data")

    try:
        with open(os.path.join(dataPath, "manifest.txt"), "r", encoding="utf-8") as fh:
            oldDate, _, oldManifest = fh.read().partition("\n")
    except:
        raise

    updateDataFiles(path=dataPath)

    try:
        with open(os.path.join(dataPath, "manifest.txt"), "r", encoding="utf-8") as fh:
            _, _, newManifest = fh.read().partition("\n")
    except:
        raise
    if oldManifest == newManifest:
        # No change
        print(f"Manifest is unchanged since {oldDate}, nothing to be committed")
        return

    diffFiles = diffManifest(oldManifest, newManifest)

    os.chdir(scriptPath)
    print(subprocess.check_output("git add data", shell=True))
    print(
        subprocess.check_output(
            f"git commit -m 'update {len(diffFiles)} files: {', '.join(diffFiles)}'",
            shell=True,
        )
    )
    print(subprocess.check_output("git push", shell=True))


def updateDataFiles(path):
    bikeshed.constants.quiet = 0
    bikeshed.update.update(path=path, manifestMode="skip")


def diffManifest(old, new):
    oldLines = set(old.split("\n"))
    newLines = set(new.split("\n"))
    diffLines = oldLines ^ newLines
    diffFiles = set(line.partition(" ")[2] for line in diffLines)
    return sorted(diffFiles)


if __name__ == "__main__":
    main()
