======
Oudjat
======


A search application based on Google's API Custom Search and Django. You can create your personal search engine, schedule jobs and manage your searches through a Django interface.


Install
-------


Setting up the Google API
-------------------------

1. Create a google account.

2. Create a custom search engine and take not of the search engine ID at http://www.google.com/cse/all

3. Identify your application to google by creating a API key which is the developer's key at https://code.google.com/apis/console/

For more informations, check the Google Custom Search documentation : https://developers.google.com/custom-search/v1/getting_started?hl=en


Schedule search jobs
----------------------

Create cron which executes the file launch_search.py everyday, with the API key created.

Open crontab to edit: 

	crontab -e

Add the following cron: 

	0 0 * * * /usr/bin/python projectpath/src/oudjat/manage.py projectpath/src/oudjat/search/management/commands/launch_search.py your_developer_key


Manage through your Django interface
------------------------------------


* Admin interface 

You can add a new domain with the matching search engine ID, activate/deactivate a search...

See at http://localhost:8000/admin


* Web interface 

You can add new searches with the matching word and domain, view activated searches or results...

See at http://localhost:8000/search







