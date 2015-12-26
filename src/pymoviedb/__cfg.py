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

from __meta__ import (
    __title__ as __title,
    __summary__ as __summary,
    __url__ as __url,
    __version__ as __ver,
    __author__ as __author,
    __email__ as __email,
    __license__ as __license,
)

dirs_file = 'dir.list'
list_file = 'movies.list'
err_file  = 'err.list'

imdb_file = '.imdb'

info_file = 'info.json'

_ignored = ['lost+found']

folder_regex = "^[a-z0-9.,\-_&?'!:;]+$"

_exts = [".ogg", ".avi", ".flv", ".mkv", ".mp4", ".m4v", ".wmv"]

force_regen = False

quiet       = True
