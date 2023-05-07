import time
import gspread
import pandas as pd
import json

b = """

                      <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:v2="http://webservice.timocom.com/schema/connect/v2">
                      <soap:Header/>
                      <soap:Body>
                      <v2:FindCargoOffersRequest version="2.6.0">
                       <v2:authentication>{pas}</v2:authentication>""".format(pas='')
b+="""

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

class a:
    def __init__(self):
        self.dic={'qwe':{1:2,3:4}}

def b(dic):
    print(dic)
    time.sleep(2)
    print(dic)
a=a()
import threading
threading.Thread(target=b,args=(a.dic,)).start()
a.dic['qweqw']='qweqweqw'
exit()


cread_file = 'service.json'
gc = gspread.service_account(cread_file)
database = gc.open("search")
wks = database.worksheet(("Sheet1"))


def request_database():
    asd = pd.DataFrame(wks.get_all_values(), dtype=str).fillna('')
    col = [i.lower().replace(' ', '') for i in asd.iloc[0].values.tolist()]
    asd.columns = col
    asd = asd.drop([0]).reset_index(drop=True)

    dic = {}

    lis_truck = asd['truck'].tolist()
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

    return dic


print(request_database())
