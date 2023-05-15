import threading

import requests
import json
import gspread
import pandas as pd
import unidecode
import xmltodict
from update_block_list import update as get_block_list
from datetime import datetime, timedelta
from datetime import time as timee
from threading import Thread, Lock
from mail_function import mail_function

# import pyperclip
with open('pas.txt', 'r') as f:
    pas = f.read()
with open('js.json', 'r') as f:
    info = json.load(f)
#try:
#    with open('list_mail.json', 'r') as f:
#        public_dict = json.load(f)
#except Exception as e:
public_dict={}
#try:
#    with open('block_list.json', 'r') as f:
#        di = json.load(f)
#except:
#    block_list_country = []
#    block_list = []

loading_block,company_country_block,company_id_block = [],[],[]
get_block_list(loading_block,company_country_block,company_id_block,abc=1)

Thread(target=get_block_list,args=(loading_block,company_country_block,company_id_block)).start()




#publick_dic_lock = Lock()
stop_event=threading.Event()


def stop():
    while True:
        now = datetime.now().time()
        start_time = timee(hour=7, minute=30)
        end_time = timee(hour=19)
        q=0
        if start_time <= now <= end_time:
            try:

                #if q:

                stop_event.set()
                q = 0

            except:
                pass
        else:
            try:
                q=1
                stop_event.clear()
            except:
                pass
Thread(target=stop).start()
#stop_event.set()
def time_now():
    return ((datetime.now()).isoformat()[:]+'Z[UTC]' )


def Creatbase():
    # if datetime.isoweekday(datetime.now()) == 1:
    #    return (datetime.now() - timedelta(days=3)).isoformat()[:-3] + 'Z'
    # if datetime.isoweekday(datetime.now()) == 6:
    #    return (datetime.now() - timedelta(days=2)).isoformat()[:-3] + 'Z'
    # if datetime.isoweekday(datetime.now()) == 7:
    #    return (datetime.now() - timedelta(days=3)).isoformat()[:-3] + 'Z'
    #
    return ((datetime.now() - timedelta(minutes=10)).isoformat()[:] )


def freight_search(info: dict):

    stop_event.wait()
    print('ok')

    lock_imap = Lock()
    lock_smtp = Lock()
    pull_id = []
    lock_list = Lock()
    lock_for_mail = Lock()

    #try:
    #    list_mail = public_dict[threading.current_thread().name]

    #except:
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

    def searching_id(even: threading.Event, param={}):
        def main_text(params={}):
            # params= {'date_earliest': '4.05', 'date_latest': '', 'unloading': {}, 'loading': {'FR': ['22', '22+40'], 'ES': []}}
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
                       
                       """
            if params['date_earliest'] == '':
                params['date_earliest']=datetime.now().date()
            if  params['date_latest'] == '' or params['date_latest'] ==params['date_earliest']:
                b+=f"""<v2:date>
                <v2:individualDates>
                <v2:date>{params['date_earliest']}</v2:date>
                <v2:date>{params['date_earliest']}</v2:date>
                <v2:date>{params['date_earliest']}</v2:date>
                <v2:date>{params['date_earliest']}</v2:date>
                <v2:date>{params['date_earliest']}</v2:date>
                </v2:individualDates>
                </v2:date>"""
            else:

                b += f"""<v2:date>
                 <v2:dateInterval>
                       <v2:start>{params['date_earliest']}</v2:start>
                       <v2:end>{params['date_latest']}</v2:end>
                       </v2:dateInterval>
                       </v2:date>"""
            t = 1
            for i in params['loading']:
                for y in params['loading'][i]:
                    if "+" in y:
                        t = 0
            if t == 0:
                for i in params['loading']:
                    for y in params['loading'][i]:
                        area = y.split("+")
                        if len(area) != 2:
                            t = 1
                            continue

                    b += f"""<v2:startLocation>

                <v2:areaSearch> 
                <v2:country>{i}</v2:country>
                <v2:postalCode>{area[0]}</v2:postalCode>

                <v2:areaInKilometres>{area[1]}</v2:areaInKilometres>
                </v2:areaSearch>
                </v2:startLocation>
                """
                    t = 0
                    break

            elif t == 1:
                if params['loading'] != {}:
                    b += """
                           <v2:startLocation>
                       <v2:countrySearch>"""
                    for k, v in params['loading'].items():

                        b += f"""

                       <v2:searchLine>
                       <v2:country>{k}</v2:country>
                       """
                        if v != []:
                            b += """<v2:postalCodes>"""
                            for i in v:
                                b += f"""<v2:postalCode>{i}</v2:postalCode>"""
                            b += """</v2:postalCodes>"""
                        b += """


                       </v2:searchLine>

                       """
                    b += """</v2:countrySearch>"""
                    b += """</v2:startLocation>
                    """
            t = 1
            for i in params['unloading']:
                for y in params['unloading'][i]:
                    if "+" in y:
                        t = 0
            if t == 0:
                for i in params['unloading']:
                    for y in params['unloading'][i]:
                        area = y.split("+")
                        if len(area) != 2:
                            t = 1
                            continue

                    b += f"""<v2:startLocation>

                            <v2:areaSearch> 
                            <v2:country>{i}</v2:country>
                            <v2:postalCode>{area[0]}</v2:postalCode>

                            <v2:areaInKilometres>{area[1]}</v2:areaInKilometres>
                            </v2:areaSearch>
                            </v2:startLocation>
                            """
                    t = 0
                    break
            elif t == 1:
                if params['unloading'] != {}:
                    b += """
                        <v2:destinationLocation>
                    <v2:countrySearch>"""
                    for k, v in params['unloading'].items():

                        b += f"""
                        
                    <v2:searchLine>
                    <v2:country>{k}</v2:country>
                    """
                        if v != []:
                            b += """<v2:postalCodes>"""
                            for i in v:
                                b += f"""<v2:postalCode>{i}</v2:postalCode>"""
                            b += """</v2:postalCodes>"""
                        b += """
    
    
                    </v2:searchLine>
    
                    """
                    b += """</v2:countrySearch>"""
                    b += """</v2:destinationLocation>
                    """
            b += "<v2:vehicleProperties>"
            b += """<v2:property>
            <v2:category>VEHICLE_BODY</v2:category>"""
            b += """<v2:values>
<v2:value>TAUTLINER</v2:value>
<v2:value>CURTAIN_SIDER</v2:value>
</v2:values>
"""

            b += "</v2:property>"
            b += """<v2:property>
            <v2:category>VEHICLE_TYPE</v2:category>"""
            b += """<v2:values>
<v2:value>TRAILER</v2:value>
</v2:values>
"""
            b += "</v2:property>"
            b += "</v2:vehicleProperties>"
            b += """

                    </v2:payload>
                    </v2:FindCargoOffersRequest>
                    </soap:Body>
                    </soap:Envelope>"""

            # exit()
            return b

        def send_request(idd=0, creat_time=Creatbase(), querry=time_now()):
            if even.is_set():
                # (threading.current_thread().name)
                exit()
            if stop_event.is_set()==0:
                list_mail = []
                if idd==0:
                    try:
                        stop_event.wait()

                        for i in range(1, 4):
                            Thread(target=send_request, args=(idd + i,),
                                   name=threading.current_thread().name).start()
                    except:
                        pass

                else:
                    exit()


            url = r"https://webservice.timocom.com/tcconnect/ws_v2/soap1_2"


            qwe = requests.post(url, text_req.format(creat=creat_time, query=querry, start=idd * 30))

            dir = (xmltodict.parse(qwe.text))
            #print(text_req)


            #print(unidecode.unidecode(str(dir)))

            try:
                if isinstance(dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload'][
                                  'ns2:entity'], list) == 0:
                    dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload'][
                        'ns2:entity'] = [dir['env:Envelope']['env:Body']['ns2:FindCargoOffersResponse']['ns2:payload'][
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


                    try:
                        if i['ns2:vehicleProperties']['ns2:property'][4]['ns2:values'] != None and 'ns2:value' in \
                                i['ns2:vehicleProperties']['ns2:property'][4]['ns2:values']:
                            if 'ADR_EQUIPMENT_SET' in i['ns2:vehicleProperties']['ns2:property'][4]['ns2:values'][
                                'ns2:value']:

                                continue
                    except Exception as e:
                        pass


                    try:
                        if float(i['ns2:lengthInMetres']) < 12:

                            continue
                    except:
                        pass
                    try:
                        if float(i['ns2:weightInTons']) < 10:

                            continue
                    except:
                        pass


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
                                   'ns2:deepLink', 'ns2:logisticsDocumentTypes', 'ns2:additionalInformationList',
                                   'ns2:otherBodyPossible', 'ns2:acceptPriceProposals']}
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
            # pyperclip.copy(qwe.text)
            qwe = parsing(qwe.text)

            for i in qwe:
                try:
                    print(i)
                    if i['customer']['companyAddress']['country'] in company_country_block:
                        continue
                except Exception as e:
                    pass
                try:
                    if str(i['customer']['publicId']) in company_id_block:
                        continue
                except Exception as e:

                    pass

                with lock_for_mail:
                    if i in list_mail:
                        pass
                    else:
                        list_mail.append(i)
                        Thread(target=send_mail, name=threading.current_thread().name, args=(i,)).start()

        def send_mail(param):
            def parsing_for_mail():
                topik = "TIMOCOM-OFFER: "
                customer = param['customer']
                contact_person = param['contactPerson']
                text = f"TIMOCOM ID: 21296\n\nCompany: Coltrans sp. z.o.o.\n\nContact person: {info['name']}\n\n"
                try:
                    if info['phone'] != "":
                        text += f"Phone: {info['phone']}\n\n"
                except:
                    pass
                full_name = ""
                try:
                    full_name += f"{contact_person['firstName']}"
                except:
                    pass
                try:
                    full_name += " " + f"{contact_person['lastName']}"
                except:
                    pass

                text += f"Provider: {customer['publicId']}, {customer['name']}, {full_name}\n\n"

                if "phone" in contact_person:
                    text += f"Phone number: {contact_person['phone']}\n\n"
                try:
                    text += f"Tax: {customer['taxId']}\n\n"
                except:
                    pass

                tt = []
                max = 1
                try:
                    for i in param['loadingPlaces']:
                        count = 0
                        for y in i['address']:
                            if y == "geocode":
                                continue
                            count += len(i["address"][y])
                        try:
                            count += len(i["loadingType"])
                        except:
                            pass
                        if count > max:
                            max = count
                except:
                    pass

                tt = ""
                load = 0
                unload = 0
                max += 5
                qq=0

                for i in param['loadingPlaces']:
                    earliestLoadingDate = None
                    latestLoadingDate = None
                    adress = i["address"]
                    if i['loadingType'] == "LOADING":

                        load += 1
                        tt = f"Loading: {adress['country']}, {adress['postalCode']} {adress['city']}"

                    else:
                        unload += 1
                        tt = f"Unloading: {adress['country']}, {adress['postalCode']} {adress['city']}"
                    try:

                        try:
                            earliestLoadingDate = i['earliestLoadingDate'][8:10] + "." + i['earliestLoadingDate'][
                                                                                         5:7] + "." + i[
                                                                                                          'earliestLoadingDate'][
                                                                                                      :4]

                            latestLoadingDate = i['latestLoadingDate'][8:10] + "." + i['latestLoadingDate'][5:7] + "." + \
                                                i['latestLoadingDate'][:4]
                        except:
                            try:
                                if earliestLoadingDate == None:
                                    earliestLoadingDate = i['date']
                            except:
                                pass
                        try:
                            tt += " " * (3 + max - len(tt)) + earliestLoadingDate
                            tt += " - " + latestLoadingDate
                        except:
                            pass
                    except:
                        pass
                    text += tt
                    text += "\n"
                    if load and qq:
                        if earliestLoadingDate != None:
                            if latestLoadingDate == None:
                                topik += f"({earliestLoadingDate}) "
                            else:
                                topik += f"({earliestLoadingDate} - {latestLoadingDate}) "
                        qq=0

                text += "\n"
                adress = param['loadingPlaces'][0]["address"]
                topik += f"{adress['country']}, {adress['postalCode']} {adress['city']} ---> "
                adress = param['loadingPlaces'][-1]["address"]
                topik += f"{adress['country']}, {adress['postalCode']} {adress['city']}"

                if 'distanceInKilometres' in param:
                    text += f"Distance in km: {param['distanceInKilometres']}\n\n"

                text += f"Length: {param['lengthInMetres']} m\n\n"

                text += f"Weight/to: {param['weightInTons']} to\n\n"

                # text+=f"Loading places: {load}\n\n"

                # text+=f"Unloading places: {unload}\n\n"

                try:
                    text += f"Price: {param['price']}\n\n"
                except:
                    pass

                vechicle = param['vehicleProperties']['property']
                # [{"category": "VEHICLE_BODY", "values": {"value": "CURTAIN_SIDER"}},
                # {"category": "VEHICLE_BODY_PROPERTY", "values": ""},
                # {"category": "VEHICLE_SWAP_BODY", "values": ""},
                # {"category": "VEHICLE_LOAD_SECURING", "values": {"value": "LASHING_STRAPS"}},
                # {"category": "VEHICLE_EQUIPMENT", "values": ""},
                # {"category": "VEHICLE_TYPE", "values": {"value": ["TRAILER", "WAGGON_AND_DRAG"]}}]}
                Vehicle_Property = {"VEHICLE_BODY": "Vehicle body", "VEHICLE_BODY_PROPERTY": "Body characteristics",
                                    "VEHICLE_EQUIPMENT": "Equipment ", "VEHICLE_LOAD_SECURING": "Load securing",
                                    "VEHICLE_SWAP_BODY": "Swap bodies", "VEHICLE_TYPE": "Vehicle type"}
                proper = {"VEHICLE_BODY": {"BOX": "Box ", "CAR_TRANSPORTER": "Car transporter",
                                           "CHASSIS": "Container chassis", "COIL_WELL": "Coil trough",
                                           "CURTAIN_SIDER": "Curtain ", "DRAWER": "Skip loader",
                                           "DUMP_TRAILER": "Tipper ", "EXTENDABLE_TRAILER": "Extendable trailer",
                                           "FLATBED": "Flatbed truck", "INLOADER": "Inloader ", "JUMBO": "Jumbo ",
                                           "LOW_LOADER": "Low loader", "MEGA": "Mega ", "MOVING_FLOOR": "Walking floor",
                                           "MOVING_FLOOR_FILL_MATERIAL": "Walking floor  (Bulk material)",
                                           "PLATFORM": "Drop side", "REFRIGERATOR": "Refrigerator ",
                                           "SEMI_TRAILER_WITH_INCLINED_TABLE": "Semi-trailer  with inclined table",
                                           "SILO": "Silo trailer", "SPECIAL_TRUCK": "Special truck",
                                           "SWAP_BODY_TRUCK": "Swap body truck", "TANK": "Tank trailer",
                                           "TAUTLINER": "Tautliner ", "THERMO": "Thermo ",
                                           "TIPPER_ROLL_OFF": "Roll-on roll-off tipper ", "TRACTOR_UNIT": "Tractor ",
                                           "VAN_CAR": "Panel van"},
                          "VEHICLE_BODY_PROPERTY": {"AIR_SUSPENDED": "Air suspension", "BACK_TIPPER": "Back tipper",
                                                    "CODE_XL": "Code XL", "DOUBLE_EVAPORATOR": "Dual evaporator",
                                                    "DOUBLE_FLOOR": "Double floor", "ELEVATING_ROOF": "Lifting roof",
                                                    "FOLDING_SIDE_BOX": "Folding side box ",
                                                    "HANGING_GARMENT_CONTAINER": "Hanging garment container ",
                                                    "LONG_TRUCK": "Euro combi", "LOW_FLOOR": "Low floor",
                                                    "LOW_LOADING_RAILS": "Steel rails for Joloda rollers ",
                                                    "REMOVAL_VAN": "Removal truck", "SIDE_TIPPER": "Side tipper",
                                                    "SLIDING_CURTAIN": "Curtainsider ", "SLIDING_ROOF": "Sliding roof",
                                                    "WIDENABLE": "Widenable"},
                          "VEHICLE_SWAP_BODY": {"FORTY_FEET_CONTAINER": "40ft Container",
                                                "FORTY_FIVE_FEET_CONTAINER": "45ft Container",
                                                "HALFPIPE_DUMPER": "Skip ",
                                                "ROLL_ON_ROLL_OFF_CONTAINER": "Roll-on roll-off container ",
                                                "SWAP_BODY": "Demountable body",
                                                "TWENTY_FEET_CONTAINER": "20ft Container"},
                          "VEHICLE_TYPE": {"TRAILER": "Articulated truck", "VEHICLE_UP_TO_12_T": "Vehicle up to 12 t ",
                                           "VEHICLE_UP_TO_3_5_T": "Vehicle up to 3.5 t ",
                                           "VEHICLE_UP_TO_7_5_T": "Vehicle up to 7.5 t ",
                                           "WAGGON_AND_DRAG": "Rigid truck"},
                          "VEHICLE_LOAD_SECURING": {"ANTI_SLIP_MATS": "Anti slip mats ", "BOARD_WALL": "Side panels",
                                                    "EDGE_PROTECTION": "Edge protection",
                                                    "LASHING_STRAPS": "Lashing straps", "LOCKING_BAR": "Locking bar",
                                                    "PALLET_STOP_BAR": "Pallet retaining bar ",
                                                    "PERFORATED_BATTEN": "Perforated batten",
                                                    "STANCHIONS": "Stanchions ", "TENSION_CHAIN": "Lashing chains"},
                          "VEHICLE_EQUIPMENT": {"ACCESS_RAMP": "Access ramp ", "ADR_EQUIPMENT_SET": "ADR ",
                                                "A_PLATE": "Waste carrier licence ",
                                                "CUSTOMS_SEAL_STRING": "Customs seal string ",
                                                "ESCORT_VEHICLE_TYPE_3": "Escort vehicle type 3 ",
                                                "ESCORT_VEHICLE_TYPE_4": "Escort vehicle type 4 ",
                                                "FIXED_LOADING_CRANE": "Fixed loading crane ",
                                                "MEAT_HOOK": "Meat hooks", "PARTITION_WALL": "Partition wall",
                                                "PORTABLE_FORKLIFT": "Portable forklift",
                                                "PORTABLE_PUMP_TRUCK": "Pallet lifter",
                                                "SATELLITE_TRACKING": "Satellite tracking",
                                                "SECOND_DRIVER": "2nd driver", "TAIL_LIFT": "Tail lift",
                                                "TARPAULIN_COVER": "Tarpaulin cover",
                                                "WOOD_STANCHIONS": "Log stanchions"}}
                t = ""

                for i in vechicle:
                    try:
                        if i['values'] != "" and i['values'] != " " and i['values'] != {} and i['values'] != [] and i[
                            'values'] != None:
                            if isinstance(i['values']['value'], str):
                                i['values']['value'] = [i['values']['value']]

                            t += f"{Vehicle_Property[i['category']]}: "

                            for y in i['values']['value']:

                                a = proper[i['category']][y].replace('  ', ' ')
                                if a[-1] == " ":
                                    a = a[:-1]
                                t += f"{a}, "
                            if t[-2:] == ", ":
                                t = t[:-2]
                            t += '\n'
                    except:
                        pass
                try:
                    if len(t) > 5:
                        text += f"Vehicle:\n{t}\n"
                except:
                    pass
                try:
                    text += f"Remark:\n{param['publicRemark']}\n\n"
                except:
                    pass
                return text, topik

            add_text = dd.dic[threading.current_thread().name]['text']
            customer = param['customer']
            contact_person = param['contactPerson']
            if 'lastName' in contact_person == 0:
                contact_person['lastName'] = ''
            if 'firstName' in contact_person == 0:
                contact_person['firstName'] = ''
            text = add_text + "\n\n" * bool(len(add_text))
            t, topik = parsing_for_mail()
            text += t
            mail_function(info, param["contactPerson"], topik, text, lock_smtp, lock_imap)

        text_req = main_text(param)
        for i in range(3):
            Thread(target=send_request, name=threading.current_thread().name, args=(i,)).start()

    # get_sheets and get_car_by_car:
    from Data import Data

    event = {}
    dd = Data(cread_file=info['cread_file'])

    for i in dd.dic:
        event[i] = threading.Event()
        # for y in dd[i]:
        Thread(target=searching_id, args=(event[i], dd.dic[i]['param'].copy(),), name=i).start()

    def update():
        new_dic = dd.get()
        if new_dic == {}:
            for k in dd.dic.keys():
                event[k].set()
            dd.dic = {}
            return
            #
        for k in dd.dic.keys():
            if (k in new_dic.keys()) == 0:
                event[k].set()
                del dd.dic[k]

        for k, v in new_dic.items():
            if (k in dd.dic) == 0:
                dd.dic[k] = v
                event[k] = threading.Event()
                Thread(target=searching_id, args=(event[k], v['param'].copy(),), name=k).start()


            else:
                if v['param'] != dd.dic[k]['param']:
                    event[k].set()
                    del event[k]
                    event[k] = threading.Event()
                    Thread(target=searching_id, args=(event[k], v['param'].copy(),), name=k).start()
                    dd.dic[k]['param'] = v['param']
                elif v['text'] != dd.dic[k]['text']:
                    dd.dic[k]['text'] = v['text']

    import time


    #def save():
    #    while True:
    #        try:
    #            if (stop_event.is_set()) ==0:
    #                list_mail=[]
    #                stop_event.wait()
    #            time.sleep(3)
    #            with publick_dic_lock:
    #                if (threading.current_thread().name in public_dict) == 0:
    #                    public_dict[threading.current_thread().name] = []
    #                for i in list_mail:
    #                    if (i in public_dict[threading.current_thread().name])==0:
    #                        public_dict[threading.current_thread().name].append(i)
    #
    #                with open('list_mail.json', 'w') as f:
    #                    json.dump(public_dict, f)
    #        except Exception as e:
    #            pass
    #Thread(target=save, name=threading.current_thread().name).start()
    while True:

        try:
            stop_event.wait()
        except:
            pass
        try:

            time.sleep(2)
            update()
        except:
            pass

    # receive update_block_list.py wgm - change
    # dd['wgm'] = new_param
    # event['wgm'].set()
    # e = threading.Event()
    # for y in dd['wgm']:
    #    Thread(target=searching_id, args=(dd['wgm'][y], e,), name='wgm')
    # event['wgm'] = e


for i in info:
    Thread(target=freight_search, args=(info[i],), name=i).start()






