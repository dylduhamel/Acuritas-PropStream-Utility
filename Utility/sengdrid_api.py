import os
import base64
from dotenv import load_dotenv
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType
from Utility.lead_database import Session, Lead
from datetime import date
from sqlalchemy import or_

def email_csv():
    # Load .env file
    load_dotenv()

    # Initialize the session
    session = Session()

    # Query for values added today
    today = date.today()
    #today = "09/27/2023" # If you want to skiptrace date other than today 

    leadData = session.query(Lead).filter(Lead.date_added == today, 
                                             Lead.first_name_owner != None, 
                                             Lead.first_name_owner != '', 
                                             Lead.phone_number_1 != None, 
                                             Lead.phone_number_1 != ''
    )

    # Convert query results to dataframes
    df1 = pd.DataFrame([{column: getattr(lead, column) for column in Lead.__table__.columns.keys()} for lead in leadData])

    if not df1.empty:
        # Get the list of current column names
        cols = list(df1.columns)

        # Remove 'first_name_owner' and 'last_name_owner' from their current positions in the list
        cols.remove('first_name_owner')
        cols.remove('last_name_owner')

        # Add 'first_name_owner' and 'last_name_owner' at the desired positions
        cols.insert(2, 'first_name_owner')  # at index 2 
        cols.insert(3, 'last_name_owner')   # at index 3

        # Reorder the dataframe according to the modified list of column names
        df1 = df1[cols]

    # Convert DataFrames to CSV and save
    csv_filepath1 = "./Data/csv_exports/data.csv"
    csv_filename1 = "data.csv"
    df1.to_csv(csv_filepath1, index=False)

    # Load SendGrid API key and email addresses
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL") 
    TO_EMAIL = os.getenv("TO_EMAIL")  
    TO_EMAIL_SELF = os.getenv("TO_EMAIL_SELF")

    # Read CSV data and convert to Base64
    with open(csv_filepath1, "rb") as f:
        data1 = base64.b64encode(f.read()).decode()

    # Create attachments
    attachment1 = Attachment(
        FileContent(data1),
        FileName(csv_filename1),
        FileType('text/csv')
    )

    # Create message
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=(TO_EMAIL, TO_EMAIL_SELF),
        subject='Sending CSV Data',
        plain_text_content='Hey Gents,\n\n\tHere is all of the data pulled in the last 24 hours.'
    )

    message.attachment = attachment1

    # Create SendGrid client
    sg = SendGridAPIClient(SENDGRID_API_KEY)

    # Send email
    response = sg.send(message)

    print(response.status_code)