from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabtools import require
import fabtools

env.hosts = ['localhost']


def install_requirements():
   """ 
   Installing required packages
   """
   # if not fabtools.python.is_pip_installed():
   #    fabtools.python.install_pip()

   # fabtools.python.install_requirements('/home/adilla/Bureau/oudjat/requirements.txt', use_sudo=True)
   
   # local('python setup.py install')

   # if not fabtools.python.is_installed('django-jenkins'):
   #    fabtools.python.install('django-jenkins', use_sudo=True)
   
   # if not fabtools.python.is_installed('coverage'):
   #    fabtools.python.install('coverage', use_sudo=True)

   # if not fabtools.python.is_installed('MySQL-python'):
   #    fabtools.python.install('MySQL-python', use_sudo=True)
 

   local('pip install --use-mirrors -r /home/adilla/Bureau/oudjat/requirements.txt')
   local('python setup.py install')
   local('pip install django-jenkins coverage MySQL-python')
 

def run_tests():
   """ 
   Running tests with Coverage and unittest
   """

   local('python src/oudjat/manage.py jenkins report search')
   local('pylint -f parseable src/oudjat/search | tee reports/pylint.report')
   local('pylint -f parseable src/oudjat/report | tee -a reports/pylint.report')



def do_all():
   install_requirements()
   run_tests()


