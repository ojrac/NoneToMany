#!/usr/bin/python
""" Dirty, dirty deploy script. """

from subprocess import call

call(["mv", "eliza/eliza.sqlite", "eliza/eliza.sqlite.tmp"])
call(["rsync", "-avz", ".", "eliza.iad01.hubspot-networks.net:/usr/share/hubspot/webapps/eliza"])
call(["mv", "eliza/eliza.sqlite.tmp", "eliza/eliza.sqlite"])
