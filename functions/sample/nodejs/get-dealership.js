const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');


function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
        
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    
    let dbListPromise = getAllRecords(cloudant,'dealerships');
    let resultOfDealership = getMatchingRecords(cloudant, 'dealerships', { st: {'$eq': params.st }});
    
    if(params.st) {
        
        console.log({ resultOfDealership });
        return resultOfDealership;
        
    }else{
         console.log({ dbListPromise });
         return dbListPromise;
    }
    
}

 /*
 Sample implementation to get all the records in a db.
 */
function getAllRecords(cloudant,dbname) {
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({ db: "dealerships", includeDocs: true, limit: 10})
        .then((result)=>{
            console.log({ result: JSON.stringify(result, null, 4) });
            resolve({result:result.result.rows});
            
        })
        .catch((error) => {
            console.log(error);
            if (error.status===404 || error.massage==='Object Not Found') {
                reject({ 404: 'The Data base is empty' });
                
            }
            else {
                reject({ 500: 'Something went wrong on the server' });
                
            }
            
        });
        
    })
    
}


/* Sample implementation to get the selected records in a db. */

function getMatchingRecords(cloudant,dbname, selector) {
    return new Promise((resolve, reject, _error) => {
        cloudant.postFind({db:"dealerships",selector:selector})
        .then((result)=>{
            console.log({ result: JSON.stringify(result, null, 4) });
            resolve({result:result.result.docs});
        
             
        })
        .catch((error) => {
            console.log(error);
            if (error.status===404 || error.statusText==='OK'|| error.statusText==='Object Not Found') {
                reject({ 404: 'The State does not exist' });
            }
            else {
                reject({500: 'Something went wrong on the server' });
                
            }
            
        });
        
    })
    
}
 

try {
    let params = {
        COUCH_URL:"https://----------bluemix.cloudantnosqldb.appdomain.cloud",
        IAM_API_KEY: "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwW"
        
    };

    main(params)
    .then((result) => {
        console.log({ result });

    })
    .catch(error => console.log(error));
    }
    catch(err) {
        console.log(error);
        
    }

