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

import argparse
import sys

import __cfg

from __pymoviedb import __pymoviedb_init, __pymoviedb_check, __pymoviedb_do

if (__name__ == "__main__"):
  global args

  parser = argparse.ArgumentParser()

  parser.add_argument("action", help="action", choices=["init", "check", "do"])

  parser.add_argument("-v", "--verbose", help="be more verbose", action="store_true")

  args = parser.parse_args()

  if args.verbose:
    __cfg.__verbose = True

  if args.action == "init":
    __pymoviedb_init()
  elif args.action == "check":
    __pymoviedb_check()
  elif args.action == "do":
    __pymoviedb_do()

  exit()
