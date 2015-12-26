
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

import glob
import os
import shutil
import subprocess
import tempfile
import pkg_resources
import json

from appdirs import AppDirs
from operator import itemgetter, attrgetter

import __cfg

def _cfg_folder():
  return AppDirs(__cfg.__title, __cfg.__author).user_data_dir

def _cfg_dirs_file():
  return _cfg_folder() + os.sep + __cfg.dirs_file

def _cfg_list_file():
  return _cfg_folder() + os.sep + __cfg.list_file

def _cfg_err_file():
  return _cfg_folder() + os.sep + __cfg.err_file

def _cfg_imdb_file(m):
  return m[0] + m[1] + os.sep + __cfg.imdb_file

def _cfg_info_file(m):
  return m[0] + m[1] + os.sep + __cfg.info_file

# http://stackoverflow.com/a/5032238/2873157
def make_sure_path_exists(path):
  try:
    os.makedirs(path)
  except OSError as exception:
    if exception.errno != errno.EEXIST:
      raise

def _file_exists(fname):
  if os.path.isfile(fname):
    return True
  else:
    return False

def copy_pkg_resource(source, dest):
  fp = tempfile.NamedTemporaryFile(delete=False)
  fp.write(pkg_resources.resource_string(__name__, source))
  fp.close()

  try:
    shutil.copyfile(fp.name, dest)
  except Exception as arg:
    print ( "unable to copy package resource '%s' to '%s'" % (source, dest) )
    print ( arg )
    exit(-1)

  try:
    os.remove(fp.name)
  except Exception as arg:
    # tmp files will be removed at reboot
    pass

def _get_folders():
  if _file_exists(_cfg_dirs_file()) == False:
    print( "%s does not exist!" % _cfg_dirs_file() )
    print("are you sure you have _init_'ed???")
    exit(-1)

  with open(_cfg_dirs_file(), "r") as f:
    f_lines = f.readlines()

  for k, v in enumerate(f_lines):
    f_lines[k] = v.strip("\r\n")

  # ret
  f_list = []

  for movies_dir in f_lines:
    if os.path.isdir(movies_dir) == False:
      print ("dir \"%s\" doesn't exist! skipping." % movies_dir)
      continue

    if movies_dir.startswith('#'):
      continue

    if movies_dir.endswith(os.sep) == False:
      movies_dir = movies_dir + os.sep

    for f in glob.iglob(movies_dir + "*"):
      if (os.path.isdir(f)):
        _, n = f.split(movies_dir)
        if n not in __cfg._ignored:
          f_list.append([movies_dir, n])

  # sort movie list by name
  f_list = sorted(f_list, key=itemgetter(1))

  return f_list

def print_v (s):
  if __cfg.quiet == False:
    print (s, end='')

def preexec(): # Don't forward signals.
  os.setpgrp()
def getFileRes(_file):
  heights = [0, 240, 360, 480, 720, 1080, 2160]
  _file = _file.replace('"', r'\"')
  #if not __cfg.quiet:
  #  print ("\tfile: " + _file)
  #  print ("\t res:",end='')

  proc = subprocess.Popen('exiftool -j -ImageWidth -ImageHeight "' + _file + '"', stdout=subprocess.PIPE, shell=True, preexec_fn = preexec)
  py2output = proc.stdout.read()
  jdec = json.loads(py2output.decode("utf-8"))
  if 'ImageWidth' and 'ImageHeight' in jdec[0].keys():
    for h in heights:
      if h >= jdec[0]['ImageHeight']:
        break;
    #if not pyme_cfg.quiet:
    #  print (str(h) + 'p')
    return str(h) + 'p'
  else:
    #if not pyme_cfg.quiet:
    #  print ('NA')
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

def getFileMatches(_dir, exts):
  ret = None
  for root, directories, filenames in os.walk(_dir):
    for filename in filenames:
      if os.path.join(root,filename).endswith(exts):
        ret = os.path.join(root,filename)
        break
  return ret
