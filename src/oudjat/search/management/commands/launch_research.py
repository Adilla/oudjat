
from django.core.management.base import NoArgsCommand, CommandError
from search.models import *
from report.models import *
from apiclient.discovery import build
import json
import pprint
import re, os, shutil, urllib
from django.utils import timezone


class Command(NoArgsCommand):
    help = 'Launches all researches'

    def handle_noargs(self, **options):

        # try:
        #     os.mkdir('/home/adilla/Bureau/tmp_research_files/')
        # except OSError:
        #     print 'Could not create new directory'
            
        service = build("customsearch", "v1",
                        developerKey="AIzaSyBGCWOxtQZomkXAVSLmyg1XI_obyTe5P4E")

        for word in Word.objects.all():
            w = word.expression
                    

            # res = service.cse().list(
            #     q = w,
            #     cx = '006966613857663466729:_k1q5ucd9eg',
            #  #   cx = dkey
            #     )

            # with open('/home/adilla/Bureau/'+ w + '_1', 'w') as f:
            #     json.dump(res, f, indent = 4)
             
            # if 'queries' in res:
            #     tmp = res['queries']
                
            #     cmpt = 2
                
            #     if 'nextPage' in tmp:
            #         tmp = res['queries']['nextPage'][0]['startIndex']
            #         next_response = service.cse().list(
            #             q = w,
            #             cx = '006966613857663466729:_k1q5ucd9eg',
            #      #       cx = key
            #             num = 10,
            #             start = tmp,
            #             ).execute()
            #         with open('/home/adilla/Bureau/' + w + '_' + str(cmpt), 'w') as f:
            #             json.dump(next_response, f, indent = 4)

            

            cmpt = 1
       
            while True:
                str_cmpt = str(cmpt)
                if os.path.exists('/home/adilla/Bureau/' + w +'_' + str_cmpt):
                    f = open('/home/adilla/Bureau/'+ w + '_' + str_cmpt, 'r')
                        
                    t = json.load(f)
                        
                    i = 0
                    print '/home/adilla/Bureau/'+ w + '_' + str_cmpt
                    if 'items' in t:
                        print len(t["items"])
                        while (i < len(t["items"])):
                            test = t["items"][i]["link"]
                            test2 = t["items"][i]["displayLink"]
                            string = re.sub('http://' + test2 + '/', '', test)
                            print string
                          
                            occ = 0
                            # ppage = urllib.urlopen('http://' + test2 + '/' + test)
           
                            # for strpage in ppage.readlines():
                            #     if strpage is not None: 
                            #       #  print strpage
                            #         try:
                            #             num = (strpage.decode('utf-8')).find(w)
                            #             if num > 0:
                            #                 occ = occ + 1
                            #         except UnicodeDecodeError:
                            #             print 'error for ' + strpage
  
                            Page.objects.get_or_create(path = string, 
                                                       sitename = test2)
                            p = Page.objects.get(path = string, sitename = test2)
                            
                            ww = Word.objects.get(expression = w)
                            r = Result(word = ww, page = p, occurences = occ, date = timezone.now())
                            r.save()
                            
                            
                            i = i + 1
                            
                            f.close()
                #    os.remove('/home/adilla/Bureau/' + w + '_' + str_cmpt)
                            cmpt = cmpt + 1
                    else:
                        cmpt = cmpt + 1
                            
                else:
                    break


                # try:
                #     os.rmdir('/home/adilla/Bureau/tmp_research_files/')
                # except OSError:
                #     print 'Could not delete directory'
                
                    
        
                    

 
