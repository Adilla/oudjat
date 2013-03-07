from django.core.management.base import NoArgsCommand, CommandError
from search.models import *
from report.models import *
from apiclient.discovery import build
import json
import pprint
import re



class Command(NoArgsCommand):
    help = 'Launches all researches'

    def handle_noargs(self, **options):

 
        service = build("customsearch", "v1",
                        developerKey="AIzaSyBGCWOxtQZomkXAVSLmyg1XI_obyTe5P4E")

        string = ''
        for word in Word.objects.all():
            w = word.expression
            res = service.cse().list(
                q = w,
                cx = '006966613857663466729:_k1q5ucd9eg',
                )
       
            with open('/home/adilla/Bureau/'+w, 'r') as f:
                t = json.load(f)
                 
                print t.keys()
                
                i = 0
                while (i < len(t["items"])):
                    test = t["items"][i]["link"]
                    test2 = t["items"][i]["displayLink"]
                    string = re.sub('http://' + test2 + '/', '', test)
                    print string
                    Page.objects.get_or_create(path = string, 
                                               sitename = test2)
                           
                    i = i + 1

                    
  
                    

 
