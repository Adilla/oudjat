""" 
Command for job 
"""

from django.core.management.base import NoArgsCommand
from search.models import Word, Domain, Research, Crontab 
from report.models import Page, Result
from apiclient.discovery import build
import re, os, json
from django.utils import timezone


class Command(NoArgsCommand):

    """
    Command launching all researches 
    """

    def handle_noargs(self, **options):
            
        """ Job handling all researches """

        service = build("customsearch", "v1",
                        developerKey="AIzaSyBGCWOxtQZomkXAVSLmyg1XI_obyTe5P4E")


        # Getting the cron to be runned (with priority = 0) 
        # and the related researches
        day_cron = Crontab.objects.get(priority = 0)
        related_researches = Research.objects.filter(cron = day_cron)


        for research in related_researches:
            print research

            # launching each research not yet done
            if research.is_done == False:
                _word = research.words
                dkey = Domain.objects.filter(researches__words = _word)
           
                res = service.cse().list(
                    q = _word,
                    #cx = '006966613857663466729:_k1q5ucd9eg',
                    cx = dkey[0].key
                    ).execute()
            
                research.is_done = True
                research.save()

                # putting the results in file with Json format
                with open('/home/adilla/Bureau/'+ _word + '_1', 'w') as _file:
                    json.dump(res, _file, indent = 4)
                
                cmpt = 1
                
                while True:
                    str_cmpt = str(cmpt)

                    # for each file, loads the content and gets all url found
                    # then adds them into the database
                    if os.path.exists(
                        '/home/adilla/Bureau/'+ _word +'_'+ str_cmpt):
                        
                        _file = open(
                            '/home/adilla/Bureau/'+ _word +'_'+ str_cmpt,'r')
                        
                        loaded_file = json.load(_file)
                        
                        i = 0
                        
                        print '/home/adilla/Bureau/'+ _word + '_' + str_cmpt
                        if 'items' in loaded_file:
                            print len(loaded_file["items"])
                            while (i < len(loaded_file["items"])):
                                test = loaded_file["items"][i]["link"]
                                test2 = loaded_file["items"][i]["displayLink"]
                            
                                check = test.find('https')
                                check2 = test.find('http')
                                if check >= 0:
                                    string = re.sub(
                                        'https://'+ test2 +'/', '', test)

                                elif check2 >= 0:
                                    string = re.sub(
                                        'http://' + test2 + '/', '', test)
                                    
                                print string
                                    
                                occ = 0
                                # ppage = urllib.urlopen(
                                # 'http://' + test2 + '/' + test)
                                
                                # for strpage in ppage.readlines():
                                #     if strpage is not None: 
                                #       #  print strpage
                                #         try:
                                #             num = (
                                #strpage.decode('utf-8')).find(w)
                                #             if num > 0:
                                #                 occ = occ + 1
                                #         except UnicodeDecodeError:
                                #             print 'error for ' + strpage
                                
                      
                                Page.objects.get_or_create(path = string, 
                                                           sitename = test2)
                                
                                _page = Page.objects.get(path = string, sitename = test2)
                                
                                _word2 = Word.objects.get(expression = _word)
                                    
                                Result.objects.get_or_create(word = _word2, 
                                                             page = _page, 
                                                             occurences = occ, 
                                                             date = timezone.now())
                                   
                                    
                                i = i + 1
                                    
                                _file.close()
                                if os.path.exists(
                                    '/home/adilla/Bureau/'+ _word +'_'+ str_cmpt):
                                    os.remove(
                                        '/home/adilla/Bureau/' + _word +'_'+ str_cmpt)
                                    cmpt = cmpt + 1
                                            
                        else:
                            cmpt = cmpt + 1   
                        
                    else:
                        break
        

        # changes to priority of each cron
        for cron in Crontab.objects.all():
            cron.priority = (cron.priority - 1) % Crontab.objects.count() 
            print cron.pk
            print cron.priority
            cron.save()
                              
                    
        
                    

 
