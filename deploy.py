#!/usr/bin/python
""" Dirty, dirty deploy script. """

from subprocess import call

call(["rsync", "-avz", ".", "eliza.iad01.hubspot-networks.net:/usr/share/hubspot/webapps/eliza"])
