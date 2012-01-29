#!/usr/bin/env python

from distutils.core import setup
from DistUtilsExtra.command import *

import re
import glob
from subprocess import Popen, PIPE

# update version.py
try:
    line = open("debian/changelog").readline()
    m = re.search(r'\((.+?)\) ([^;]+);', line)
    VERSION = m.group(1)
    CODENAME = open("CODENAME").readline().strip()
    DISTRO = Popen(["lsb_release", "-s", "-i"], stdout=PIPE).communicate()[0].strip()
    RELEASE = Popen(["lsb_release", "-s", "-r"], stdout=PIPE).communicate()[0].strip()
    open("kazam/version.py","w").write("""VERSION='%s'
CODENAME='%s'
DISTRO='%s'
RELEASE='%s'
""" % (VERSION, CODENAME, DISTRO, RELEASE))
except:
    VERSION='0.1'
    CODENAME='maverick'
    DISTRO='Ubuntu'
    RELEASE='10.04'

# real setup
setup(name="kazam", version=VERSION,
      scripts=["bin/kazam"
               ],
      packages = ['kazam',
                  'kazam.pulseaudio',
                  'kazam.backend',
                  'kazam.backend.export_sources',
                  'kazam.frontend',
                 ],
      data_files=[
                  ('share/kazam/ui/',
                   glob.glob("data/ui/*ui")),
                  ('share/kazam/images/',
                   glob.glob("data/images/*svg")),
                  ('share/kazam/ui/export_sources/',
                   glob.glob("data/ui/export_sources/*.ui")),
                  ],
      cmdclass = { "build" : build_extra.build_extra,
                   "build_i18n" :  build_i18n.build_i18n,
                   "build_help" : build_help.build_help,
                   "build_icons" : build_icons.build_icons}
      )
