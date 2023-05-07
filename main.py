import threading

import requests
import json
import gspread
import pandas as pd
import unidecode
import xmltodict
from datetime import datetime, timedelta
from threading import Thread, Lock
import pyperclip
with open('pas.txt','r') as f:
    pas=f.read()










class time_now:
    def __str__(self):
        return datetime.now().isoformat()[:-3] + 'Z'


class Creatbase:
    def __str__(self):
        if datetime.isoweekday(datetime.now()) == 1:
            return (datetime.now() - timedelta(days=3)).isoformat()[:-3] + 'Z'
        if datetime.isoweekday(datetime.now()) == 6:
            return (datetime.now() - timedelta(days=2)).isoformat()[:-3] + 'Z'
        if datetime.isoweekday(datetime.now()) == 7:
            return (datetime.now() - timedelta(days=3)).isoformat()[:-3] + 'Z'

        return (datetime.now() - timedelta(days=1)).isoformat()[:-3] + 'Z'


def freight_search():
    pull_id = []
    lock_list = Lock()
    lock_for_mail = Lock()
    list_mail = []

    # def send_mail(dir):
    #    global list_today
    #    list_today.append(dir)
    #    for i in lis:
    #        dir=xmltodict.parse(timmo_get(i))
    #
    #        dir=dir['env:Envelope']['env:Body']['ns2:LookupCargoOffersResponse']['ns2:payload']['ns2:entity']
    #        del dir['ns2:publicId']
    #        del dir["ns2:creationDateTime"]
    #        del dir['ns2:deepLink']
    #        send_mail(dir)
    #        # creat picking not succsesfull shot Thread

    def searching_id(even : threading.Event, param={}):
        def main_text(params={}):
            #params= {'date_earliest': '4.05', 'date_latest': '', 'unloading': {}, 'loading': {'FR': ['22', '22+40'], 'ES': []}}
            b = """

                                  <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:v2="http://webservice.timocom.com/schema/connect/v2">
                                  <soap:Header/>
                                  <soap:Body>
                                  <v2:FindCargoOffersRequest version="2.6.0">
                                   <v2:authentication>{pas}</v2:authentication>""".format(pas=pas)
            b += """
    
                       <v2:payload xsi:type="v2:CargoOfferFilterType"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                       <v2:updatedAfterDateTime>{creat}</v2:updatedAfterDateTime>
                     <v2:queryDateTime>{query}</v2:queryDateTime>
                     <v2:sortings>
                       <v2:sorting>
                       <v2:field>creationDateTime</v2:field>
                       <v2:ascending>false</v2:ascending>
                       </v2:sorting>
                       </v2:sortings>
                     <v2:firstResult>{start}</v2:firstResult>
                       <v2:maxResults>30</v2:maxResults>
                       <v2:date>
                       <v2:dateInterval>"""
            b+=f""" 
                       <v2:start>{params['date_earliest']}</v2:start>
                       <v2:end>{params['date_latest']}</v2:end>
                       </v2:dateInterval>
                       </v2:date>"""
            if params['loading']!={}:
                b+="""
                       <v2:startLocation>
                   <v2:countrySearch>"""
                for k,v in params['loading'].items():

                    b+=f"""
                       
                   <v2:searchLine>
                   <v2:country>{k}</v2:country>
                   """
                    if v!=[]:
                        b+="""<v2:postalCodes>"""
                        for i in v:
                            b+=f"""<v2:postalCode>{i}</v2:postalCode>"""
                        b+="""</v2:postalCodes>"""
                    b+="""
    
    
                   </v2:searchLine>
    
                   """
                b+="""</v2:countrySearch>"""
                b+="""</v2:startLocation>
                """
            if params['unloading']!={}:
                b+="""
                    <v2:destinationLocation>
                <v2:countrySearch>"""
                for k,v in params['unloading'].items():

                    b+=f"""
                    
                <v2:searchLine>
                <v2:country>{k}</v2:country>
                """
                    if v!=[]:
                        b+="""<v2:postalCodes>"""
                        for i in v:
                            b+=f"""<v2:postalCode>{i}</v2:postalCode>"""
                        b+="""</v2:postalCodes>"""
                    b+="""


                </v2:searchLine>

                """
                b+="""</v2:countrySearch>"""
                b+="""</v2:destinationLocation>
                """
            b+="<v2:vehicleProperties>"
            b+="""<v2:property>
            <v2:category>VEHICLE_BODY</v2:category>"""
            b+="""<v2:values>
<v2:value>TAUTLINER</v2:value>
<v2:value>CURTAIN_SIDER</v2:value>
</v2:values>
"""
            b+="</v2:property>"
            b+="""<v2:property>
            <v2:category>VEHICLE_TYPE</v2:category>"""
            b+="""<v2:values>
<v2:value>TRAILER</v2:value>
</v2:values>
"""
            b+="</v2:property>"
            b+="</v2:vehicleProperties>"
            b+="""

                    </v2:payload>
                    </v2:FindCargoOffersRequest>
                    </soap:Body>
                    </soap:Envelope>"""
            return b
        
        def send_request(idd=0, creat_time=str(Creatbase()), querry=str(time_now())):

            if even.is_set():
                print(threading.current_thread().name)
                exit()
            
            url = r"https://webservice.timocom.com/tcconnect/ws_v2/soap1_2"
            qwe = requests.post(url, text_req.format(creat=creat_time, query=querry, start=idd * 30))
            dir = (xmltodict.parse(qwe.text))
            
            try:
                if isinstance(dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload'][
                           'ns2:entity'], list)==0:
                    dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload'][
                           'ns2:entity']=[dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload'][
                           'ns2:entity']]
            except Exception as e:
                pass
                
            
            try:

                if len(dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload'][
                           'ns2:entity']) == 30 and idd % 3 == 0 and idd > 0:
                    for i in range(1, 4):
                        Thread(target=send_request, args=(idd + i, creat_time, querry),
                               name=threading.current_thread().name).start()
            except Exception as e:
                # print(e)
                pass

            if idd == 0:
                try:
                    creat_time_ = \
                        dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload']['ns2:entity'][0][
                            "ns2:creationDateTime"]
                except:
                    creat_time_ = creat_time
                try:
                    Thread(target=send_request, args=(0, creat_time_,), name=threading.current_thread().name).start()
                except Exception as e:
                    pass
            list_get = []
            
            try:
                for i in dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload']['ns2:entity']:
                    public_id = i["ns2:publicId"]
                    if i['ns2:vehicleProperties']['ns2:property'][4]['ns2:values']!=None and 'ns2:value' in  i['ns2:vehicleProperties']['ns2:property'][4]['ns2:values'] :
                            if 'ADR_EQUIPMENT_SET' in  i['ns2:vehicleProperties']['ns2:property'][4]['ns2:values']['ns2:value']:
                                    continue
                    # loading = i['ns2:loadingPlaces']['ns2:loadingPlace'][0]['ns2:address']["ns2:country"] + \
                    #          i['ns2:loadingPlaces']['ns2:loadingPlace'][0]['ns2:address']["ns2:postalCode"]
                    # date_1 = i['ns2:loadingPlaces']['ns2:loadingPlace'][0]["ns2:earliestLoadingDate"]
                    # date_2 = i['ns2:loadingPlaces']['ns2:loadingPlace'][0]["ns2:latestLoadingDate"]
                    # unloadding = i['ns2:loadingPlaces']['ns2:loadingPlace'][-1]['ns2:address']["ns2:country"] + \
                    #             i['ns2:loadingPlaces']['ns2:loadingPlace'][-1]['ns2:address']["ns2:postalCode"]

                    list_get.append(public_id)

                    # with lock_list:
                    #    if ('24.04' in list_public_id) == 0:
                    #        list_public_id['24.04'] = []
                    #        list_public_id['24.04'].append(public_id)
                    # with lock_list:
                    #    if public_id in list_public_id['24.04']:
                    #        continue
                    #    else:
                    #        list_public_id['24.04'].append(public_id)

                    # print(xmltodict.parse(timmo_get(id)))


            except Exception as e:
                pass
                # return 0, creat, diq
            # return creat, diq
            if list_get != []:
                timmo_get(list_get)

        def searching_start():
            r1 = None
            lock = Lock()
            for i in range(3):
                if i % 3 == 0:
                    Thread(target=send_request(i))

                    lock.acquire()

        def timmo_get(public_id_list):
            
            def parsing(text: dict):
                def change(dir):

                    if isinstance(dir, dict):
                        dir2 = {}
                        for i in dir:
                            if i[:4] == 'ns2:':
                                dir2[i[4:]] = change(dir[i])
                            else:

                                dir2[i] = change(dir[i])

                        return dir2
                    elif isinstance(dir, list):
                        dir2 = []
                        for i in range(len(dir)):
                            dir2.append(change(dir[i]))
                        return dir2
                    elif isinstance(dir, str):
                        if dir[:4] == 'ns2:':
                            return dir[4:]
                        return dir

                text = xmltodict.parse(text)
                try:
                    text = text['env:Envelope']['env:Body']['ns2:LookupCargoOffersResponse']['ns2:payload'][
                        'ns2:entity']
                except:
                    return []
                if isinstance(text, list) == 0:
                    text = [text]
                lis_del = {'del': ["ns2:publicId", "ns2:creationDateTime", 'ns2:trackable', 'ns2:contactChannels',
                                   'ns2:vehicleProperties', 'ns2:deepLink', 'ns2:logisticsDocumentTypes',
                                   'ns2:otherBodyPossible', 'ns2:additionalInformationList',
                                   'ns2:acceptPriceProposals']}
                for i in range(len(text)):
                    try:
                        del text[i]['ns2:customer']['@xsi:type']
                        text[i]['ns2:loadingPlaces'] = text[i]['ns2:loadingPlaces']['ns2:loadingPlace']
                        text[i]['ns2:contactPerson'] = text[i]['ns2:contactPerson']['ns2:detail']
                        text[i]['ns2:customer'] = text[i]['ns2:customer']['ns2:detail']
                    except:
                        pass
                    try:
                        text[i]['ns2:price'] = text[i]['ns2:price']['ns2:amount'] + ' ' + text[i]['ns2:price'][
                            'ns2:currency']
                    except:
                        pass
                    for y in lis_del['del']:
                        try:
                            del text[i][y]

                        except:
                            pass

                # print(text)
                return change(text)

            if public_id_list == []:
                exit()
            payload2_get = """ <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:v2="http://webservice.timocom.com/schema/connect/v2">
                <soap:Header/>
                <soap:Body>
         <v2:LookupCargoOffersRequest version="2.6.0">
           <v2:authentication>{pas}</v2:authentication>
           <v2:payload xsi:type="v2:PublicIdsFilterType"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
           <v2:publicIds>
           """.format(pas=pas)
            with lock_list:

                pull_id_ = pull_id.copy()
                pull_id.extend(public_id_list)

            for i in public_id_list:
                if i in pull_id_:
                    continue

                payload2_get += """
            <v2:publicId>{id}</v2:publicId>""".format(id=i)

            payload2_get += """
               </v2:publicIds>
               </v2:payload>
             </v2:LookupCargoOffersRequest>
             </soap:Body>
                 </soap:Envelope>
             """
            """"""

            url = r"https://webservice.timocom.com/tcconnect/ws_v2/soap1_2"
            qwe = requests.post(url, payload2_get.encode("UTF-8"), headers={
                'content-type': 'application/soap+xml; charset=UTF-8'
            })
            qwe=parsing(qwe.text)

            with lock_for_mail:

                for i in qwe:
                    if i in list_mail:
                        pass
                    else:
                        list_mail.append(i)
                        Thread(target=send_mail, name=threading.current_thread().name, args=(i,)).start()

        def send_mail(info):
            print(unidecode.unidecode(str(info)))
        
        text_req = main_text(param)
        for i in range(3):
            Thread(target=send_request, name=threading.current_thread().name, args=(i,)).start()

    # get_sheets and get_car_by_car:
    from Data import Data
    
    event = {}
    dd=Data()
    

    for i in dd.dic:
        event[i] = threading.Event()
        # for y in dd[i]:
        Thread(target=searching_id, args=(event[i], dd.dic[i]['param'].copy(),  ), name=i).start()
    def update():
        new_dic = dd.get()
        if new_dic=={}:
            for k in dd.dic.keys():
                event[k].set()
            dd.dic={}
            return
            #
        for k in dd.dic.keys():
            if (k in new_dic.keys()) ==0:
                event[k].set()
                del dd.dic[k]
                

        for k,v in new_dic.items():
            if (k in dd.dic) ==0:
                dd.dic[k]=v
                event[k]=threading.Event()
                Thread(target=searching_id, args=(event[k],v['param'].copy(),), name=k).start()

                
            else:
                if v['param'] !=dd.dic[k]['param']:
                    event[k].set()
                    del event[k]
                    event[k]=threading.Event()
                    Thread(target=searching_id, args=(event[k], v['param'].copy(),), name=k).start()
                    dd.dic[k]['param']=v['param']
                elif v['text'] !=dd.dic[k]['text']:
                    dd.dic[k]['text']=v['text']
    import time
    print('ok')
    while True:
        time.sleep(5)
        update()

    
    
    
    # receive update wgm - change
    #dd['wgm'] = new_param
    #event['wgm'].set()
    #e = threading.Event()
    #for y in dd['wgm']:
    #    Thread(target=searching_id, args=(dd['wgm'][y], e,), name='wgm')
    #event['wgm'] = e
freight_search()