import threading

import requests
import json
import gspread
import pandas as pd
import unidecode
import xmltodict
from datetime import datetime, timedelta
from threading import Thread, Lock
#import pyperclip
class Data:
    
    def __init__(self, cread_file='service.json'):
        self.cread_file = cread_file
        self.gc = gspread.service_account(self.cread_file)
        self.database = self.gc.open("search")
        self.wks = self.database.worksheet(("Sheet1"))
        self.dic = {}
        self.get(1)

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
            if asd.iloc()[lis1[i - 1]]['ready?']!='TRUE':
                continue
            

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
                locks[k].set()
                del self.dic[k]
                

        for k,v in new_dic.items():
            if (k in self.dic) ==0:
                self.dic[k]=v
                locks[k]=threading.Event()
                Thread(target=searching_id, args=(v['param'].copy(),locks[k]), name=k).start()

                
            else:
                if v['param'] !=self.dic[k]['param']:
                    locks[k].set()
                    locks[k]=threading.Event()
                    Thread(target=searching_id, args=(v['param'].copy(),locks[k]), name=k).start()
                    
                elif v['text'] !=self.dic[k]['text']:
                    self.dic[k]['text']=v['text']
                    #event? no

