#!/usr/bin/env python

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

from __future__ import print_function

import glob
import fnmatch
import json
import os
from operator import itemgetter, attrgetter

import omdb

import pyme_cfg
from   pyme_helpers import getFileRes, which, getFileMatches

movie_dirs = []
movie_list = []
err_lines  = set()
dat = {}
movies = {}

f_lines = []

if os.path.exists(pyme_cfg.list_file):
  with open(pyme_cfg.list_file, "r") as f:
    f_lines = f.readlines()

for l in f_lines:
  l = (l).strip("\r\n")
  l_s = l.split('|')
  movies[l_s[1]] = l

for folder in open(pyme_cfg.dirs_file):
  movie_dirs.append(folder.strip("\r\n"))

# get all folders
for movie_dir in movie_dirs:
  if os.path.isdir(movie_dir) == False:
    if not pyme_cfg.quiet:
      print ("dir '" + movie_dir + "' doesn't exist! skipping.")
    continue
  for f in glob.iglob(movie_dir + "*"):
    if (os.path.isdir(f)):
      _, n = f.split(movie_dir)
      if n not in pyme_cfg._ignored:
        movie_list.append([movie_dir, n])

# sort movie list by name
movie_list = sorted(movie_list, key=itemgetter(1))

# main iter
for movie in movie_list:
  _dir, _name, _cur_dir = movie[0], movie[1], os.getcwd()

  if not pyme_cfg.quiet:
    print ("processing: " + _name)

  dat['base'] = _name

  # resolution
  dat['res'] = 'NA'
  if which('exiftool') is not None:
    match = getFileMatches(_dir + _name, tuple(pyme_cfg._exts))
    if match is not None:
      dat['res'] = getFileRes(match)

  # search
  s_title = _name.replace("_", " ")

  imdbid = False
  res    = None
  skip   = False
  jsondb = None
  if os.path.isfile(_dir + _name + '/' + pyme_cfg.imdb_file):
    with open(_dir + _name + '/' + pyme_cfg.imdb_file) as f: imdbid = f.read()
    imdbid = imdbid.strip("\r\n")
  if pyme_cfg.force_regen == True or not os.path.isfile(_dir + _name + '/' + pyme_cfg.info_file):
    if not pyme_cfg.quiet:
      print ('\tnetwork : omdb ...', end='')
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
      jsondb = json.loads(res.content)
    else:
      jsondb = None
  else: # force_regen == false
    if not pyme_cfg.quiet:
      print ('\tnetwork : file ...', end='')
    with open(_dir + _name + '/' + pyme_cfg.info_file) as f: jsondb = json.loads(f.read())

  if not pyme_cfg.quiet:
    print ("done!")  # network

  if skip or 'Error' in jsondb.keys():
    print ("\tskipping " + _name)
    err_lines.add("skipping " + _name + "\n")
  else:
    dat['Title']      = jsondb['Title']
    dat['imdbID']     = jsondb['imdbID']
    dat['Year']       = jsondb['Year']
    dat['Released']   = jsondb['Released']
    dat['imdbRating'] = jsondb['imdbRating']
    dat['Language']   = jsondb['Language']
    t_str = dat['Title'] + "|" + dat['imdbID']  + "|" + dat['Released'] + "|" + dat['res'] + "|" + dat['imdbRating'] + "|" + dat['Language']
    if not pyme_cfg.quiet:
      print ('\t' + t_str)
    movies[dat['imdbID']] = t_str
    with open(_dir + _name + '/' + pyme_cfg.info_file, 'w') as f:
      json.dump(dat, f)

movies = sorted(movies.items(), key=itemgetter(1))
with open(pyme_cfg.list_file, "w") as f:
  for movie in movies:
    f.write((movie[1] + "\n").encode('utf-8'))

with open(pyme_cfg.err_file, "w") as f:
  f.writelines(sorted(err_lines))
