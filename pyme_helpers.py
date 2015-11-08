# Copyright (c) 2015 - thewisenerd <thewisenerd@protonmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import pyme_cfg

import os
import subprocess
import json
def getFileRes(_file):
  heights = [0, 240, 360, 480, 720, 1080, 2160]
  _file = _file.replace('"', r'\"')
  if not pyme_cfg.quiet:
    print "\tfile: " + _file
    print "\t res:",
  proc = subprocess.Popen('exiftool -j -ImageWidth -ImageHeight "' + _file + '"', stdout=subprocess.PIPE, shell=True)
  py2output = proc.stdout.read()
  jdec = json.loads(py2output)
  if 'ImageWidth' and 'ImageHeight' in jdec[0].keys():
    for h in heights:
      if h >= jdec[0]['ImageHeight']:
        break;
    if not pyme_cfg.quiet:
      print str(h) + 'p'
    return str(h) + 'p'
  else:
    if not pyme_cfg.quiet:
      print 'NA'
    return 'NA'

def which(program):
  import os
  def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

  fpath, fname = os.path.split(program)
  if fpath:
    if is_exe(program):
      return program
  else:
    for path in os.environ["PATH"].split(os.pathsep):
      path = path.strip('"')
      exe_file = os.path.join(path, program)
      if is_exe(exe_file):
        return exe_file
  return None

import os
def getFileMatches(_dir, exts):
  ret = None
  for root, directories, filenames in os.walk(_dir):
    for filename in filenames:
      if os.path.join(root,filename).endswith(exts):
        ret = os.path.join(root,filename)
        break
  return ret
