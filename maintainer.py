import os
from sh import git

_BOT_USERNAME = os.environ["RODABOX_BOT_USERNAME"]
_TOKEN_GITHUB = os.environ["RODABOX_TOKEN_GITHUB"]

def pull():
  git('git pull %s:%s@https://github.com/rodaconveniencia/rodabox' % (_BOT_USERNAME, _TOKEN_GITHUB))

def issuer(title, message):
  pass
