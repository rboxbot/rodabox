import os
import json

_FILENAME = 'environ'
_FILEPATH = './.%s' % _FILENAME

def set(key, value):
  environ = dict()
  with open(_FILEPATH, 'r') as file:
    environ = json.loads(file.read())
  with open(_FILEPATH, 'w') as file:
    environ[key] = str(value)
    json.dump(environ, file, ensure_ascii=False, sort_keys=True, indent=2)
  os.environ[key] = value

def get(key=None):
  if key == None:
    return dict(os.environ)
  if not key in os.environ.keys():
    raise KeyError("There is no item named '%s' in the archive" % key)
  return os.environ[key]

def remove(key):
  environ = dict()
  with open(_FILEPATH, 'r') as file:
    environ = json.loads(file.read())
  if not key in environ.keys():
    raise KeyError("There is no item named '%s' in the archive" % key)
  with open(_FILEPATH, 'w') as file:
    environ.pop(key)
    os.environ.pop(key)
    json.dump(environ, file, ensure_ascii=False, sort_keys=True, indent=2)

def lazzy():
  copy = os.environ.copy()
  with open(_FILEPATH, 'r') as file:
    environ = json.loads(file.read())
  for key, value in environ.items():
    copy[key] = str(value)
  return copy
