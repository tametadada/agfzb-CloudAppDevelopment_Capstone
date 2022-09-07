# Connect to service instance by running import statements.
import sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
import simplejson


    
def main(dict):
    """
    check url,Authantication 
    """
    secret = {
        "COUCH_USERNAME": "xxxxx-xxxxx-yyyyy-zzzzz-bluemix",
        "IAM_API_KEY": "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
        "COUCH_URL": "https://wwww-bluemix.cloudantnosqldb.appdomain.cloud"
        
    }
    
    try:
        client = Cloudant.iam(
            account_name=secret["COUCH_USERNAME"],
            api_key=secret["IAM_API_KEY"],
            url=secret["COUCH_URL"],
            connect=True,
        )
    except:
        return {
            'statusCode': 500,
            'message': "Something went wrong on the server"
            }
            
    database=client["reviews"]
    
    try:
        selector = {'dealership': {'$eq': int(dict["id"])}}
        # result_by_filter=database.get_query_result(selector,raw_result=True)
        result= {
        'headers':{'Content-Type':'application/json'},
        'body':{'data':response}
        }
        return result
    except:
        return {
            'statusCode': 404,
            'message': "dealerId does not exist"
            }



