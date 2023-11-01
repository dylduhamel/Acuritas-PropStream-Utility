'''
Function to skiptrace data from SQL DB

Queries for only those values with "date_added" == curr_date()

Saves as skiptraced JSON file
'''

import os
import requests
import json
from sqlalchemy import update, or_
from Utility.lead_database import Lead, Session
from datetime import date

def skiptrace_leads(chosenDate=None):
    # API call function
    def api_call(lead_list):
        api_token = os.getenv("BATCHDATA_SKIPTRACE_API_TOKEN")
        headers = {
            'Accept': 'application/json, application/xml',
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }

        data = {"requests": []}

        for lead in lead_list:
            # Create a base data object
            data_object = {
                "propertyAddress": {
                    "city": lead.property_city,
                    "street": lead.property_address,
                    "state": lead.property_state
                }
            }

            # Add zipcode if it's not None
            if lead.property_zipcode is not None:
                data_object["propertyAddress"]["zip"] = lead.property_zipcode

            # Append to the requests list
            data["requests"].append(data_object)

        try:
            response = requests.post('https://api.batchdata.com/api/v1/property/skip-trace', headers=headers, data=json.dumps(data))
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print ("Something went wrong", err)
        
        results = response.json()

        # Return results for all leads
        return results["results"]["persons"]

    # Create a session
    session = Session()

    # Query for values added for date
    if chosenDate is None:
        chosenDate = date.today()

    leads = session.query(Lead).filter(Lead.date_added == chosenDate).all()

    # Make a single API call for all leads
    results = api_call(leads)

    # Export json to Skiptraced_data directory
    with open(f'./Data/Skiptrace/skiptrace_{chosenDate}.json', 'w') as file:
        json.dump(results, file)


"""

FIX DATE THING BECAUSE DATABASE USES DIFFERENT DATE OBJECT


"""