import requests
import json
import random
def select():
    access_token="CAACEdEose0cBAMROESdGJ28i77OE7YdX0VCoN6KNXCKuvZAsXplBvbVnfdjLa4fewy4t9yqeLBukc9tUzp3IFYvuZAMPp3YEECStfMDlhDbLeBDOfI9G1CU4t3fhsjCuj7uMwTHYDcAzoqCNXThV6IcCvBLQcqiNEkRm1gWlWmmNR3yYImDlc3MyTm3VB1gJGlAfz6uZCZCYHUj3BefZC"
    url="https://graph.facebook.com/106548149477723_639982822800917?fields=comments.limit%28200%29&access_token={0}".format(access_token)
    raw=requests.get(url)
    page=json.loads(raw.text)
    name=[]
    comm={}
    for item in page['comments']['data']:
        if item.get('message_tags') is not None:
            _n=item.get('from').get('name')
            _msg=item.get('message')
            name.append(_n)
            comm[_n]=_msg


    candidates=list(set(name))
    unique_n=list(set(name))
    selected={}
    for i in range(2):
        winner=unique_n[random.randint(0,len(unique_n)-1)]
        selected[winner]=comm.get(winner)
        unique_n.remove(winner)

    return candidates,selected

if __name__ == '__main__':
    print(select())
