from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabtools import require
import fabtools



def install_requirements():
   """ 
   Installing required packages
   """
   run('pip install -r requirements.txt')
   run('python setup.py install')
   run('pip install django-jenkins coverage MySQL-python')
 

def run_tests():
   """ 
   Running tests with Coverage and unittest
   """

   run('python src/oudjat/manage.py jenkins report search')
   run('pylint -f parseable src/oudjat/search | tee reports/pylint.report')
   run('pylint -f parseable src/oudjat/report | tee -a reports/pylint.report')



def do_all():
   install_requirements()
   run_tests()


