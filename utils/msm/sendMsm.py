from twilio.rest import Client
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse


def sendMSM(message, phoneNumber):
    try: 
        # Cargar las variables del archivo .env
        load_dotenv()
        accountSid=os.getenv("ACCOUNTSID")
        authToken=os.getenv("AUTHTOKEN")
        client = Client(accountSid,authToken)
        twilioPhoneNumber=os.getenv("PHONENUMBERTWILIO")

        message = client.messages.create(
            body =message,
            from_=twilioPhoneNumber,
            to=phoneNumber
        )
        response_content = {"message": "SMS send Successfully!"}
        return JSONResponse(content=response_content, status_code=200)
    except Exception as e:
        raise ValueError(f'{e} Error sending SMS')
