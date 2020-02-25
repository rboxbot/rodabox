import os
import json
import requests
import threading
import subprocess

import environ

from datetime import datetime
from sh import git, reboot, python, kill

def listener(self):
  pass

def ask_for_authentication(self):
  pass

def check_github_updates(self):
  pass

def backpack_service(self):
  pass

def ipc_service(self):
  pass

def pinpad_service(self):
  pass

if __name__ == '__main__':
  os.environ = environ.lazzy()

  environ.set('RODA_TESTE', 'liks')
  print(environ.get('RODA_TESTE'))
  environ.set('RODA_TESTE', 'kling')
  print(environ.get('RODA_TESTE'))
  environ.remove('RODA_TESTE')
  print(environ.get())
