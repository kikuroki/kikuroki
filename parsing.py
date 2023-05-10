from datetime import datetime 
param={"customer": {"publicId": "424803", "name": "SUPPLY FRET SAS", "phone": "+33 4 88 13 54 04", "companyAddress": {"country": "FR", "postalCode": "84140", "city": "AVIGNON", "streetOrPostbox": "BP 61225 - 546 RUE BARUCH DE SPINOZA"}, "postalAddress": {"country": "FR"}, "taxId": "FR67904047164"}, "contactPerson": {"lastName": "TUECH", "firstName": "Florent", "title": "MR", "email": "florent.tuech@supply-fret.fr", "languages": {"language": ["en", "fr"]}, "position": "president", "phone": "+33 4 88 13 54 04", "phoneMobile": "+33 6 30 83 89 82"}, "vehicleProperties": {"property": [{"category": "VEHICLE_BODY", "values": {"value": "CURTAIN_SIDER"}}, {"category": "VEHICLE_BODY_PROPERTY", "values": ""}, {"category": "VEHICLE_SWAP_BODY", "values": ""}, {"category": "VEHICLE_LOAD_SECURING", "values": {"value": "LASHING_STRAPS"}}, {"category": "VEHICLE_EQUIPMENT", "values": ""}, {"category": "VEHICLE_TYPE", "values": {"value": ["TRAILER", "WAGGON_AND_DRAG"]}}]}, "otherBodyPossible": "false", "lengthInMetres": "13.6", "weightInTons": "25.3", "loadingPlaces": [{"loadingType": "LOADING", "address": {"country": "ES", "postalCode": "31191", "city": "Beriain", "geocoded": "true"}, "earliestLoadingDate": "2023-05-10", "latestLoadingDate": "2023-05-12", "date": "2023-05-12"}, {"loadingType": "UNLOADING", "address": {"country": "FR", "postalCode": "17100", "city": "Fontcouverte", "geocoded": "true"}}], "distanceInKilometres": "453"}

info={"mail":"o","name":"Oleksii","cread_file":"service.json","phone":""}

customer=param['customer']
contact_person=param['contactPerson']
text=f"TIMOCOM ID: 21296\n\nCompany: Coltrans sp. z.o.o.\n\nContact person: {info['name']}\n\n"
if info['phone']!="":
    text+=f"Phone: {info['phone']}\n\n"
full_name=""
try:
   full_name+=f"{contact_person['firstName']}"
except:
   pass
try:
   full_name+=" "+f"{contact_person['lastName']}"
except:
   pass

text+=f"Provider: {customer['publicId']}, {customer['name']}, {full_name}\n\n"

if "phone" in contact_person:
   
    text+=f"Phone number: {contact_person['phone']}\n\n"

text+=f"Tax: {customer['taxId']}\n\n"

tt=[]
max=-1
for i in param['loadingPlaces']:
    count=0
    for y in i['address']:
        if y=="geocode":
            continue
        count+=len(i["address"][y])
    try:
        count+=len(i["loadingType"])
    except:
        pass
    if count>max:
      max=count
    
tt=""
load=0
unload=0
max+=5
for i in param['loadingPlaces']:
    earliestLoadingDate=None
    latestLoadingDate=None
    adress=i["address"]
    if i['loadingType']=="LOADING":
        load+=1
        tt=f"Loading: {adress['country']}, {adress['postalCode']} {adress['city']}"
        
    else:
        unload+=1
        tt=f"Unloading: {adress['country']}, {adress['postalCode']} {adress['city']}"
    try:
        print(max)
        print(len(tt))
        try:
            earliestLoadingDate=i['earliestLoadingDate'][8:10] +"."+ i['earliestLoadingDate'][5:7]

            latestLoadingDate=i['latestLoadingDate'][8:10]+"."+ i['latestLoadingDate'][5:7]
        except:
           pass
        try:   
            tt+=" "*(3+max-len(tt)) + earliestLoadingDate
            tt+=" - " + latestLoadingDate
        except:
           pass
    except:
        pass
    text+=tt
    text+="\n"
text+="\n"
 
if 'distanceInKilometres' in param:
    text+=f"Distance in km: {param['distanceInKilometres']}\n\n"

     


text+=f"Length: {param['lengthInMetres']} m\n\n"

text+=f"Weight/to: {param['weightInTons']} to\n\n"

#text+=f"Loading places: {load}\n\n"

#text+=f"Unloading places: {unload}\n\n"


"""
Required type of vehicle: Articulated truck

    Type of body: Tautliner, Curtain
"""
try:
    text+=f"Price: {param['price']}\n\n"
except:
 pass
try:
    text+=f"Remark:\n{param['publicRemark']}\n\n"
except:
 pass
print(text)