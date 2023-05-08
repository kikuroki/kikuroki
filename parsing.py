param={"customer": {"publicId": "424803", "name": "SUPPLY FRET SAS", "phone": "+33 4 88 13 54 04", "companyAddress": {"country": "FR", "postalCode": "84140", "city": "AVIGNON", "streetOrPostbox": "BP 61225 - 546 RUE BARUCH DE SPINOZA"}, "postalAddress": {"country": "FR"}, "taxId": "FR67904047164"}, "contactPerson": {"lastName": "TUECH", "firstName": "Florent", "title": "MR", "email": "florent.tuech@supply-fret.fr", "languages": {"language": ["en", "fr"]}, "position": "president", "phone": "+33 4 88 13 54 04", "phoneMobile": "+33 6 30 83 89 82"}, "vehicleProperties": {"property": [{"category": "VEHICLE_BODY", "values": {"value": "CURTAIN_SIDER"}}, {"category": "VEHICLE_BODY_PROPERTY", "values": ""}, {"category": "VEHICLE_SWAP_BODY", "values": ""}, {"category": "VEHICLE_LOAD_SECURING", "values": {"value": "LASHING_STRAPS"}}, {"category": "VEHICLE_EQUIPMENT", "values": ""}, {"category": "VEHICLE_TYPE", "values": {"value": ["TRAILER", "WAGGON_AND_DRAG"]}}]}, "otherBodyPossible": "false", "lengthInMetres": "13.6", "weightInTons": "25.3", "loadingPlaces": [{"loadingType": "LOADING", "address": {"country": "ES", "postalCode": "31191", "city": "Beriain", "geocoded": "true"}, "earliestLoadingDate": "2023-05-10", "latestLoadingDate": "2023-05-12", "date": "2023-05-12"}, {"loadingType": "UNLOADING", "address": {"country": "FR", "postalCode": "17100", "city": "Fontcouverte", "geocoded": "true"}}], "distanceInKilometres": "453"}


customer=param['customer']
contact_person=param['contactPerson']
text=f"""TIMOCOM ID: NASHA

Company: NASHA

Contact person: NASHA

Phone: NASHA

 

Provider: {customer['publicId']}, {customer['name']}, {contact_person['firstName']} {contact_person['lastName']}

Phone number: {contact_person['phone']}

Tax: {customer['taxId']}


Load to be offered:

    On: 05.05.2023

    Town: DE, 56068 Koblenz

 

Unloading:

Town: DE, 15230 Frankfurt (Oder)

 

Distance in km: {param['distanceInKilometres']}

     


Length: {param['lengthInMetres']} m

Weight/to: {param['weightInTons']} to

Loading places: 1

Unloading places: 1


 

Required type of vehicle: Articulated truck

    Type of body: Tautliner, Curtain
"""
try:
    text+=f"""
Price: {param['price']}
"""
except:
 pass
try:
    text+=f"""
Remark:

{param['publicRemark']}
"""
except:
 pass
 print(text)