#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import bikeshed
import os

def main():
	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
	bikeshed.config.quiet = False
	bikeshed.update.update(path=path)
	bikeshed.update.createManifest(path=path)

if __name__ == "__main__":
    main()