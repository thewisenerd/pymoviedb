#!/usr/bin/env python3

import os
import stat
import sys
import zipfile

import shutil

config = {
  "name"    : "pymoviedb",
  "source"  : [
                ["src/pymoviedb", ""],
                ["src/omdb-0.5.0/omdb", "omdb/"],
              ],
  "res"     : [
                ["binaries/dir.list.example"],
                ["src/appdirs.py", "appdirs.py"],
              ],
  "version" : "0.1.1",
  "desc"    : "pyMovieDB",
  "author"  : "thewisenerd",
  "email"   : "thewisenerd@protonmail.com",
  "url"     : "http://thewisenerd.me/",
  "keywords": ["python", "movie", "dbs"],
}

try:
  os.mkdir('dist')
except Exception as arg:
  if arg.errno == 17:
    pass
  else:
    quit(-1)

try:
  os.mkdir('build')
except Exception as arg:
  if arg.errno == 17:
    pass
  else:
    quit(-1)

def getexecname():
  return ('build/' + config['name'])

def getdistname():
  return ('dist' + os.sep + config['version'] + os.sep + config['name'])

# create zip
zf = zipfile.ZipFile(getexecname(), mode='w')

# add src
for directory in config['source']:
  fs = directory[0] #source
  fd = directory[1] #dest

  for f in os.listdir(fs):
    print ("+ src: %s: " % (fd + f), end='')
    try:
      zf.write(fs + os.sep + f, fd + f)
    except Exception as arg:
      print ('fail')
      zf.close()
      os.remove(getexecname())
      exit(1)
    print ('ok')

# add res
for ft in config['res']:
  f = ft[0]
  if (len(ft) == 1):
    fn = ft[0]
  elif (len(ft) == 2):
    fn = ft[1]

  # add to zip
  print ("+ res: %s: " % fn, end='')
  try:
    zf.write(f, fn)
  except Exception as arg:
    print ('fail')
    zf.close()
    os.remove(getexecname())
    exit(1)
  print ('ok')

# close zip
zf.close()

# copy to dist
# shutil.copyfile(getexecname(), getdistname())
print ('cp to dist/')
with open(getexecname(), 'rb') as original:
  data = original.read()

try:
  os.mkdir('dist' + os.sep + config['version'])
except Exception as arg:
  if arg.errno == 17:
    pass
  else:
    exit(-1)

with open(getdistname(), 'wb') as f:
  f.write(bytes('#!/usr/bin/env python3\n', 'UTF-8'))
  f.write(data)
  f.close()

print ('chmod ' + getdistname())
st = os.stat(getdistname())
os.chmod(getdistname(), st.st_mode | stat.S_IEXEC)

print ('cleaning build/')
shutil.rmtree('build')
