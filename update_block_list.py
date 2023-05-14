import time

import gspread
import pandas as pd

def update(loading_block,company_country_block,company_id_block, abc=0,cread_file='service.json'):
    while True:
        try:

            cread_file = cread_file
            gc = gspread.service_account(cread_file)
            database = gc.open("search")
            wks = database.worksheet(("company"))
            asd = pd.DataFrame(wks.get_all_values(), dtype=str).fillna('')
            col = [i.lower().replace(' ', '') for i in asd.iloc[0].values.tolist()]
            asd.columns = col
            asd = asd.drop([0]).reset_index(drop=True)

        except:
            pass
        asd=asd.apply(lambda x: x.astype(str).str.upper())


        try:
            loading_block.extend([i for i in asd.loc[asd['loading_check']=="NO"]['loading_code'].to_list() if (i in loading_block)==0])
        except:
            pass
        try:
            company_country_block.extend([i for i in asd['company_country_block'].to_list() if (i in company_country_block) == 0 and i!=''])
        except:
            pass
        try:
            company_id_block.extend([i for i in asd['company_id_block'].to_list() if (i in company_id_block)==0 and i!=''])
        except:
            pass

        if abc:
            return
        time.sleep(10)




