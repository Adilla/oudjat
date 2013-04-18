from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabtools import require
import fabtools

env.hosts = ['localhost']

SOURCE = 'source /usr/local/bin/virtualenvwrapper.sh'
BIN = '/bin/bash -l -c '
VENV_NAME = 'test'
WORKON = 'workon ' + VENV_NAME 

def virtualenv(venv_command, venv_name):
   with prefix('cd /home/adilla/Bureau/oudjat/'):
      local(''+ BIN + '"' + SOURCE + ' && ' + venv_command + ' ' + venv_name + '"')
   

def setup():
   """ 
   Creating new virtualenv
   """
   virtualenv('mkvirtualenv --no-site-package', VENV_NAME)


def install_requirements():
   """ 
   Installing required packages
   """
   with prefix('cd /home/adilla/Bureau/oudjat/'):
      with prefix(WORKON):
         run('pip install -r requirements.txt')
         run('python setup.py install')
 

def run_tests():
   """ 
   Running tests with Coverage and unittest
   """
   with prefix('cd /home/adilla/Bureau/oudjat/src/oudjat/'):
      with prefix(WORKON):
         run('coverage run --source=\'.\' --branch manage.py test report search')


def clean():
   """ 
   Removing created virtualenv
   """
   virtualenv('rmvirtualenv', VENV_NAME) 


def do_all():
   setup()
   install_requirements()
   run_tests()
   clean()


