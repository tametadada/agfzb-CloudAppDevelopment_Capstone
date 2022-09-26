from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main(dict):
    secret = {
        "COUCH_URL": "https://XXXXXXXXXXXXXXXXXXXXXXXXXXX-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        "COUCH_USERNAME": "KAKAKAKAKAKAKAKAKAKAKAK-bluemix"
        
    }
    
    try:
        client = Cloudant.iam(
            account_name=secret["COUCH_USERNAME"],
            api_key=screat["IAM_API_KEY"],
            connect=True,
        )
        database= client["reviews"],
        document=database.create_document(dict['review'])
        if document.exists():
            result= {
            'headers':{'Content-Type':'application/json'},
            'body':{'message':"DataInserted"}
            }
            return result
    except:
        return {
            'statusCode': 500,
            'message': "Something went wrong on the server"
            }
            
            