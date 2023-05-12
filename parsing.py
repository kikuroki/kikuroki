from datetime import datetime 

print(int(1.2))
exit()
param={"customer": {"publicId": "424803", "name": "SUPPLY FRET SAS", "phone": "+33 4 88 13 54 04", "companyAddress": {"country": "FR", "postalCode": "84140", "city": "AVIGNON", "streetOrPostbox": "BP 61225 - 546 RUE BARUCH DE SPINOZA"}, "postalAddress": {"country": "FR"}, "taxId": "FR67904047164"}, "contactPerson": {"lastName": "TUECH", "firstName": "Florent", "title": "MR", "email": "florent.tuech@supply-fret.fr", "languages": {"language": ["en", "fr"]}, "position": "president", "phone": "+33 4 88 13 54 04", "phoneMobile": "+33 6 30 83 89 82"}, "vehicleProperties": {"property": [{"category": "VEHICLE_BODY", "values": {"value": "CURTAIN_SIDER"}}, {"category": "VEHICLE_BODY_PROPERTY", "values": ""}, {"category": "VEHICLE_SWAP_BODY", "values": ""}, {"category": "VEHICLE_LOAD_SECURING", "values": {"value": "LASHING_STRAPS"}}, {"category": "VEHICLE_EQUIPMENT", "values": ""}, {"category": "VEHICLE_TYPE", "values": {"value": ["TRAILER", "WAGGON_AND_DRAG"]}}]}, "otherBodyPossible": "false", "lengthInMetres": "13.6", "weightInTons": "25.3", "loadingPlaces": [{"loadingType": "LOADING", "address": {"country": "ES", "postalCode": "31191", "city": "Beriain", "geocoded": "true"}, "earliestLoadingDate": "2023-05-10", "latestLoadingDate": "2023-05-12", "date": "2023-05-12"}, {"loadingType": "UNLOADING", "address": {"country": "FR", "postalCode": "17100", "city": "Fontcouverte", "geocoded": "true"}}], "distanceInKilometres": "453"}

info={"mail":"o","name":"Oleksii","cread_file":"service.json","phone":""}


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
            print(max)
            print(len(tt))
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
        if earliestLoadingDate != None:
            if latestLoadingDate == None:
                topik += f"({earliestLoadingDate}) "
            else:
                topik += f"({earliestLoadingDate} - {latestLoadingDate}) "

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

    return text,topik
print(parsing_for_mail())