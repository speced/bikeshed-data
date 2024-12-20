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
    #print(datetime.datetime.now(datetime.UTC))
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

    diffData = diffManifests(oldManifest, newManifest)

    if diffData["total"] == 0:
        print(f"Manifest is unchanged since {oldManifest.dt}, nothing to be committed")
        return

    os.chdir(scriptPath)
    print(subprocess.check_output("git add data", shell=True))

    command = f"git commit -m 'updated {diffData['total']} files: "
    commandBits = []
    for category in ["added", "removed", "changed"]:
        if diffData[category]:
            commandBits.append(category + " " + ", ".join(diffData[category]))
    command += "; ".join(commandBits)
    command += "'"
    print(subprocess.check_output(command, shell=True))

    print(subprocess.check_output("git push", shell=True))


def updateDataFiles(path):
    bikeshed.constants.quiet = 0
    mode = bikeshed.update.UpdateMode.MANUAL | bikeshed.update.UpdateMode.FORCE
    with bikeshed.messages.messagesSilent() as _:
        pass
    bikeshed.update.update(path=path, updateMode=mode)


def diffManifests(old, new):
    oldFiles = set(old.entries.items())
    newFiles = set(new.entries.items())
    oldPaths = set(old.entries.keys())
    newPaths = set(new.entries.keys())

    removedPaths = oldPaths - newPaths
    addedPaths = newPaths - oldPaths
    persistingPaths = oldPaths & newPaths

    changedPaths = set(file[0] for file in oldFiles ^ newFiles) & persistingPaths
    return {
        "added": sorted(addedPaths),
        "removed": sorted(removedPaths),
        "changed": sorted(changedPaths),
        "total": len(addedPaths) + len(removedPaths) + len(changedPaths),
    }


if __name__ == "__main__":
    main()
