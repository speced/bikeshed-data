#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import os
import re
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
            oldManifest = bikeshed.update.Manifest.fromString(fh.read())
    except:
        raise

    updateDataFiles(path=dataPath)

    try:
        with open(os.path.join(dataPath, "manifest.txt"), "r", encoding="utf-8") as fh:
            newManifest = bikeshed.update.Manifest.fromString(fh.read())
    except:
        raise
    if str(oldManifest) == str(newManifest):
        # No change
        print(f"Manifest is unchanged since {oldDate}, nothing to be committed")
        return

    diffData = diffManifests(oldManifest, newManifest)

    os.chdir(scriptPath)
    print(subprocess.check_output("git add data", shell=True))

    command = f"git commit -m 'updated {diffData['total']} files: "
    commandBits = []
    for category in ["added", "removed", "changed"]:
        if diffData[category]:
            commandBits.push(category + " " + ", ".join(diffData[category]))
    command += "; ".join(commandBits)
    command += "'"
    print(subprocess.check_output(command, shell=True))

    print(subprocess.check_output("git push", shell=True))


def updateDataFiles(path):
    bikeshed.constants.quiet = 0
    mode = bikeshed.update.UpdateMode.MANIFEST | bikeshed.update.UpdateMode.FORCE
    with bikeshed.messages.messagesSilent() as _:
        bikeshed.update.update(path=path, updateMode=mode)


def diffManifests(old, new):
    oldFiles = set(
        (node.props["hash"], node.props["path"])
        for node in old["manifest"].getAll("file")
    )
    newFiles = set(
        (node.props["hash"], node.props["path"])
        for node in new["manifest"].getAll("file")
    )
    oldPaths = set(file[1] for file in oldFiles)
    newPaths = set(file[1] for file in newFiles)

    removedPaths = oldPaths - newPaths
    addedPaths = newPaths - oldPaths
    persistingPaths = oldPaths & newPaths

    changedPaths = set(file[1] for file in oldFiles ^ newFiles) & persistingPaths
    return {
        "added": sorted(addedPaths),
        "removed": sorted(removedPaths),
        "changed": sorted(changedPaths),
        "total": len(addedPaths) + len(removedPaths) + len(changedPaths),
    }


if __name__ == "__main__":
    main()
