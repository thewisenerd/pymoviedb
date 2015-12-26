#! /usr/bin/env python3

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

import json
import os
import re
import pprint
import sys

import omdb

from operator import itemgetter, attrgetter

import __cfg
import __helpers

from __helpers import _cfg_folder, _cfg_dirs_file, _cfg_err_file, _cfg_list_file, _cfg_imdb_file, _cfg_info_file
from __helpers import _get_folders, print_v

def __pymoviedb_init():
  # make_sure_path_exists(_cfg_folder())
  os.makedirs(_cfg_folder(),exist_ok=True)

  # make sure dir.list doesn't already exist
  if os.path.exists(_cfg_dirs_file()):
    print( "%s already exists!" % _cfg_dirs_file() )
    print("are you sure you haven't already _init_'ed???")
    exit(-1)


  print ( "initializing %s..." % __cfg.__title )

  print_v ( "copying cfg file... " )

  __helpers.copy_pkg_resource('binaries/dir.list.example', _cfg_dirs_file())

  print_v ( "done copying!\n" )

  dirs_file_tiny = _cfg_dirs_file().replace(os.environ['HOME'], '~')
  print ( "edit %s and add your folder(s)." % dirs_file_tiny )

def __pymoviedb_check():

  # check exiftool
  if __helpers.which('exiftool') is None:
    print("`exiftool` not found! please install exiftool!")
    exit(-1)

  l = _get_folders()

  for f in l:
    match = len(re.findall( __cfg.folder_regex, f[1] ))
    if match == 0:
      print ( "please rename: \"%s%s\"" % (f[0], f[1]))

    match = __helpers.getFileMatches(("%s%s" % (f[0], f[1])), tuple(__cfg._exts))
    if match is None:
      print ( "no files found in \"%s%s\"" % (f[0], f[1]))

def __pymoviedb_do():
  global movies
  global err_lines

  movies = {}
  err_lines = set()

  if os.path.isfile(_cfg_list_file()):
    with open(_cfg_list_file()) as data_file:
      movies = json.load(data_file)

  l = _get_folders()

  for movie in l:
    _dir, _name, _cur_dir = movie[0], movie[1], os.getcwd()
    dat = {}

    print_v ( "processing: %s\n" % _name )

    dat['base'] = _name

    dat['res'] = 'NA'
    if __helpers.which('exiftool') is not None:
      match = __helpers.getFileMatches(_dir + _name, tuple(__cfg._exts))
      if match is not None:
        dat['res'] = __helpers.getFileRes(match)

    # search
    s_title = _name.replace("_", " ")

    imdbid = False
    res    = None
    skip   = False
    jsondb = None

    if os.path.isfile(_cfg_imdb_file(movie)):
      with open(_cfg_imdb_file(movie)) as f:
        imdbid = f.read()
        imdbid = imdbid.strip("\r\n")

    print ( "%s: " % _name, end='' )
    sys.stdout.flush()
    if __cfg.force_regen == True or not os.path.isfile(_cfg_info_file(movie)):
      print ( "network: ", end='' )
      sys.stdout.flush()

      if (imdbid):
        try:
          res = omdb.request(i=imdbid)
        except:
          skip = True
      else:
        try:
          res = omdb.request(t=s_title)
        except:
          skip = True

      if not skip:
        jsondb = json.loads(res.content.decode('utf-8'))
      else:
        jsondb = None
        print ( "fail", end='' )
    else: # force_regen == false
      print ( "file: ", end='' )
      sys.stdout.flush()

      with open(_cfg_info_file(movie)) as f:
        jsondb = json.loads(f.read())

      if len(jsondb) == 0:
        jsondb = None
        print ( "fail", end='' )
      else:
        print ( "ok", end='' )

    if jsondb == None or skip or 'Error' in jsondb.keys():
      print ( "...skip" )
      err_lines.add("skipping " + _name + "\n")

      # continue with next movie
      continue

    # goto next line
    print ( "\n", end='' )

    dat['Title']      = jsondb['Title']
    dat['imdbID']     = jsondb['imdbID']
    dat['Year']       = jsondb['Year']
    dat['Released']   = jsondb['Released']
    dat['imdbRating'] = jsondb['imdbRating']
    dat['Language']   = jsondb['Language']

    movies[dat['imdbID']] = dat

    with open(_cfg_info_file(movie), 'w') as f:
      json.dump(dat, f)
  # for movie in l: end

  # write moviews
  with open(_cfg_list_file(), "w") as f:
    f.write(pprint.pformat(movies, indent=2))

  # write err
  with open(_cfg_err_file(), "w") as f:
    f.writelines(sorted(err_lines))
