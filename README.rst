======
Oudjat
======


API GOOGLE.

Create a google account.
Create a custom search engine.
Identify your application to google by creating a API key.
More informations on this page : https://developers.google.com/custom-search/v1/getting_started?hl=en

Create cron which executes the file launch_research.py everyday, with the API key created

Open crontab to edit: 

Crontab -e

Add the following cron: 

0 0 * * * python your_absolute_path/oudjat/src/oudjat/manage.py your_absolute_path/oudjat/src/oudjat/search/management/command/launch_research.py your_developer_key

