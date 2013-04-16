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
   with cd('.'):
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
   

   with cd('.'), prefix(WORKON):
      # require.deb.packages([
      #       'python-dev',
      #       'libmysqlclient-dev',
      #       ])

      
      sudo('apt-get install python-dev')
      sudo('apt-get install libmysqlclient-dev')
      # require.python.package([
      #       'coverage',
      #       'rt',
      #       'django==1.4',
      #       'MySQL-python',
      #       'google-api-python-client',
      #       ])
                           
   # with cd('.'), prefix(WORKON):
 

   #    #requirement.txt ??
      run('pip install coverage')
      run('pip install rt')
      run('pip install django==1.4')
      run('pip install MySQL-python')
      run('pip install --upgrade google-api-python-client')


def run_tests():
   """ 
   Running tests with Coverage and unittest
   """
   with cd('.'), prefix(WORKON):
      run('python manage.py test report search')



def clean():
   """ 
   Removing created virtualenv
   """
 
   virtualenv('rmvirtualenv', VENV_NAME) 







def do_all():
   setup()
   install_requirements()
   #run_tests()
   clean()

