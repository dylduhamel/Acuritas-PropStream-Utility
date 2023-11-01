import datetime
import pytz

# Get current date - * Used for DB, do not modify
def curr_date():
    current_date = datetime.datetime.now(pytz.timezone('America/New_York'))
    formatted_date = current_date.strftime("%m/%d/%Y")
    return formatted_date