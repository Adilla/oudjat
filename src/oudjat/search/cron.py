import pprint
from apiclient.discovery import build

def launch_research():
    service = build("customsearch", "v1",
                    developerKey="AIzaSyBGCWOxtQZomkXAVSLmyg1XI_obyTe5P4E")

    res = service.cse().list(
        q='test',
        cx='006966613857663466729:_k1q5ucd9eg',
        ).execute()
    pprint.pprint(res)
