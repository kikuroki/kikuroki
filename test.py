import threading

import requests
import json
import gspread
import pandas as pd
import unidecode
import xmltodict
from datetime import datetime, timedelta
from threading import Thread, Lock
with open('pas.txt','r') as f:
    pas=f.read()


class Data:

    def __int__(self, cread_file='service.json'):
        self.cread_file = cread_file
        self.gc = gspread.service_account(self.cread_file)
        self.database = self.gc.open("search")
        self.wks = self.database.worksheet(("Sheet1"))
        self.data = {}
        Thread(target=self.get, args=(1,)).start()

    def reconect(self):
        self.gc = gspread.service_account(self.cread_file)
        self.database = self.gc.open("search")
        self.wks = self.database.worksheet(("Sheet1"))

    def get(self, init=0):
        asd = pd.DataFrame(self.wks.get_all_values(), dtype=str).fillna('')
        col = [i.lower().replace(' ', '') for i in asd.iloc[0].values.tolist()]
        asd.columns = col
        asd = asd.drop([0]).reset_index(drop=True)

        dic = {}

        lis_truck = asd['truck'].tolist()
        for i in range(len(lis_truck)):

            if lis_truck[i] != '' and lis_truck[i] in lis_truck[i + 1:]:
                lis_truck[i] = lis_truck[i] + '_]'
        lis1 = []
        for i in range(len(lis_truck)):
            if len(lis_truck[i]) > 0:
                lis1.append(i)
        lis1.append(len(lis_truck))

        typ_loa = [i.upper().replace(' ', '').replace('KM', '') for i in asd['type_loa'].tolist()]
        typ_un = [i.upper().replace(' ', '').replace('KM', '') for i in asd['type_un'].tolist()]
        for i in range(1, len(lis1)):
            dic_ = {}
            dic_loading = {}
            dic_unloading = {}

            dic_['date_earliest'] = asd.iloc()[lis1[i - 1]]['date_earliest']
            dic_['date_latest'] = asd.iloc()[lis1[i - 1]]['date_latest']
            lis_loading = [i.upper().replace(' ', '') for i in asd['loading'].tolist()]
            lis_unloading = [i.upper().replace(' ', '') for i in asd['unloading'].tolist()]
            lis_loading1 = []
            lis_unloading1 = []
            for y in range(lis1[i - 1], lis1[i]):
                if lis_loading[y] != '':
                    lis_loading1.append(y)
                if lis_unloading[y] != '':
                    lis_unloading1.append(y)
            lis_loading1.append(lis1[i])
            lis_unloading1.append(lis1[i])
            for y in range(1, len(lis_loading1)):
                lis = []
                for w in range(lis_loading1[y - 1], lis_loading1[y]):
                    if typ_loa[w] != '':
                        lis.append(typ_loa[w])
                if lis_loading[lis_loading1[y - 1]] in dic_loading:

                    dic_loading[lis_loading[lis_loading1[y - 1]]].extend(lis)
                else:
                    dic_loading[lis_loading[lis_loading1[y - 1]]] = lis
            for y in range(1, len(lis_unloading1)):
                lis = []
                for w in range(lis_unloading1[y - 1], lis_unloading1[y]):
                    if typ_un[w] != '':
                        lis.append(typ_un[w])
                if lis_unloading[lis_unloading1[y - 1]] in dic_unloading:

                    dic_unloading[lis_unloading[lis_unloading1[y - 1]]].extend(lis)
                else:
                    dic_unloading[lis_unloading[lis_unloading1[y - 1]]] = lis

            dic_['unloading'] = dic_unloading
            dic_['loading'] = dic_loading
            dic[lis_truck[lis1[i - 1]]] = {'param': dic_, 'text': asd.iloc()[0]['text']}
        if init:
            self.dic = dic

        return dic

    def update(self, locks: dict):
        new_dic = self.get()
        #
        for k in self.dic.keys():
            if (k in new_dic.keys()) ==0:
                #kill
                pass

        for k,v in new_dic.items():
            if (k in self.dic) ==0:
                #start new add to del list
                pass
            else:
                if v['param'] !=self.dic[k]['param']:
                    #kill
                    #start new add to del list
                    pass
                elif v['text'] !=self.dic[k]['text']:
                    self.dic[k]['text']=v['text']
                    #event? no









class time_now:
    def __str__(self):
        return datetime.now().isoformat()[:-3] + 'Z'


class Creatbase:
    def __str__(self):
        if datetime.isoweekday(datetime.now()) == 1:
            return (datetime.now() - timedelta(days=3)).isoformat()[:-3] + 'Z'

        return (datetime.now() - timedelta(days=1)).isoformat()[:-3] + 'Z'


def freight_search(param={}):
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

    def searching_id(param={}):
        def main_text(params={}):
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
                       <v2:dateInterval> 
                       <v2:start>2023-05-03</v2:start>
                       <v2:end>2023-05-10</v2:end>
                       </v2:dateInterval>
                       </v2:date>
                       <v2:startLocation>
                   <v2:countrySearch>
                   <v2:searchLine>
                   <v2:country>FR</v2:country>
    
    
                   </v2:searchLine>
    
                   </v2:countrySearch>
                   </v2:startLocation>
                  <v2:destinationLocation>
                 <v2:countrySearch>
                 <v2:searchLine>
                   <v2:country>DE</v2:country>
                  </v2:searchLine>
    
                   </v2:countrySearch>
    
                   </v2:destinationLocation>
                       </v2:payload>
                     </v2:FindCargoOffersRequest>
                     </soap:Body>
                     </soap:Envelope>"""
            return b

        def send_request(idd=0, creat_time=str(Creatbase()), querry=str(time_now())):

            # if kill then break

            url = r"https://webservice.timocom.com/tcconnect/ws_v2/soap1_2"
            qwe = requests.post(url, text_req.format(creat=creat_time, query=querry, start=idd * 30))
            dir = (xmltodict.parse(qwe.text))
            try:

                if len(dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload'][
                           'ns2:entity']) == 30 and idd % 3 == 0 and idd > 0:
                    for i in range(1, 4):
                        Thread(target=send_request, args=(idd + i, creat_time, querry),
                               name=threading.currentThread().getName()).start()
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

                Thread(target=send_request, args=(0, creat_time_,), name=threading.currentThread().getName()).start()

            list_get = []
            try:
                for i in dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload']['ns2:entity']:
                    public_id = i["ns2:publicId"]
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


            except:
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

            with lock_for_mail:

                for i in parsing(qwe.text):
                    if i in list_mail:
                        pass
                    else:
                        list_mail.append(i)
                        Thread(target=send_mail, name=threading.currentThread().getName(), args=(i,)).start()

        def send_mail(info):
            print(unidecode.unidecode(str(info)))

        text_req = main_text(param)
        for i in range(3):
            Thread(target=send_request, name=threading.currentThread().getName(), args=(i,)).start()

    # get_sheets and get_car_by_car:
    dd = {'wgm': {'param': {}}, 'wgm2': {'param': {}}}
    event = {}
    for i in dd:
        e = threading.Event()
        # for y in dd[i]:
        Thread(target=searching_id, args=(dd[i]['param'], e,), name=i)
        event[i] = e

    # receive update wgm - change
    dd['wgm'] = new_param
    event['wgm'].set()
    e = threading.Event()
    for y in dd['wgm']:
        Thread(target=searching_id, args=(dd['wgm'][y], e,), name='wgm')
    event['wgm'] = e
