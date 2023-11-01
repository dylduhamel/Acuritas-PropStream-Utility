import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DATE
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

Base = sqlalchemy.orm.declarative_base()

# Database structure
class Lead(Base):
    # The name of the database
    __tablename__ = "propstream_leads"

    id = Column(Integer, primary_key=True)
    date_added = Column(DATE)
    first_name_owner = Column(String(100))
    last_name_owner = Column(String(100))
    property_address = Column(String(200))
    property_city = Column(String(200))
    property_state = Column(String(200))
    property_zipcode = Column(String(200))
    property_county = Column(String(200))
    property_type = Column(String(200))
    phone_number_1 = Column(String(100))
    phone_number_1_type = Column(String(100))
    phone_number_2 = Column(String(100))
    phone_number_2_type = Column(String(100))
    email_1 = Column(String(200))
    email_2 = Column(String(200))
    email_3 = Column(String(200))

    # Printing representation for testing
    def __repr__(self):
        return (
            f"Lead(date_added={self.date_added}, "
            f"first_name_owner={self.first_name_owner}, "
            f"last_name_owner={self.last_name_owner}, "
            f"property_address={self.property_address}, "
            f"property_city={self.property_city}, "
            f"property_state={self.property_state}, "
            f"property_zipcode={self.property_zipcode}, "
            f"property_county={self.property_county}, "
            f"property_type={self.property_type}, "
            f"phone_number_1={self.phone_number_1}, "
            f"phone_number_1_type={self.phone_number_1_type}, "
            f"phone_number_2={self.phone_number_2}, "
            f"phone_number_2_type={self.phone_number_2_type}, "
            f"email_1={self.email_1}, "
            f"email_2={self.email_2}, "
            f"email_3={self.email_3}, "
        )


## Database credentials
db_endpoint = os.getenv("DB_ENDPOINT")
db_name = os.getenv("DB_NAME")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

engine = create_engine(f"mysql+pymysql://{username}:{password}@{db_endpoint}/{db_name}")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
