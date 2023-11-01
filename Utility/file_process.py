import pandas as pd
import warnings
from Utility.lead_database import Lead, Session

# Suppress a specific warning from openpyxl
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

def read_and_process_file(file_path):
    # Remove UNIX filepath quote if present
    file_path = file_path.strip("'")

    # Check the file extension
    file_extension = file_path.split('.')[-1]
    
    if file_extension not in ['xlsx', 'csv']:
        return 1
    
    # Create new database session
    session = Session()

    # Read the file based on its extension
    if file_extension == 'xlsx':
        data = pd.read_excel(file_path)
    elif file_extension == 'csv':
        data = pd.read_csv(file_path)
    
    # Columns mapping from the file to the Lead object attributes
    columns_mapping = {
        "Address": "property_address",
        "City": "property_city",
        "State": "property_state",
        "Zip": "property_zipcode",
        "County": "property_county",
        "Property Type": "property_type"
    }
    
    # Iterate through each row
    for index, row in data.iterrows():
        lead_data = {}
        for key, value in columns_mapping.items():
            if key in data.columns and pd.notna(row[key]):
                lead_data[value] = row[key]
        
        # Only create a Lead instance if necessary data is available
        if lead_data:
            lead_instance = Lead(
                property_address=lead_data.get("property_address", None),
                property_city=lead_data.get("property_city", None),
                property_state=lead_data.get("property_state", None),
                property_zipcode=lead_data.get("property_zipcode", None),
                property_county=lead_data.get("property_county", None),
                property_type=lead_data.get("property_type", None)
            )

            # Add lead to db
            session.add(lead_instance)


    # Add new session to DB
    session.commit()
    # Relinquish resources
    session.close()

    return 0

