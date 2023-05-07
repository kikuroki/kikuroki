params= {'date_earliest': '4.05', 'date_latest': '', 'unloading': {}, 'loading': {'FR': ['22', '22+40'], 'ES': []}}
with open('pas.txt','r') as f:
    pas=f.read()
def a(params):
     
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
print(a(params))