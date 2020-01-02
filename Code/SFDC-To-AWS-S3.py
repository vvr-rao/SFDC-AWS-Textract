#ALTERNATIVE WAY TO COPY ATTACHMENTS FROM SALESFORCE TO AWS S3

import boto3
import io
from simple_salesforce import Salesforce
import requests
import os

s3 = boto3.resource('s3')

sf = Salesforce(username='<USERNAME>', password='<PASSWORD>', 
security_token='<SESSION_TOKEN>', domain='test')

sessionId = sf.session_id
instance = sf.sf_instance

print ('sessionId: ' + sessionId)

#HARDCODED HERE FOR ILLUSTRATION
fileid = '<ATTACHMENT ID>'


attachment = sf.query("SELECT Id, Name, Body FROM Attachment where Id='" + fileid + 
"' LIMIT 1")
filename=attachment['records'][0]['Name']
print('filename: ' + filename)



response = requests.get('https://' + instance + 
'/services/data/v39.0/sobjects/Attachment/' + fileid + '/body',
headers = {  'Authorization': 'Bearer ' + sessionId })

#OPTIONAL - CAN USE TO SAVE LOCALLY
#f1 = open(filename, "wb")
#f1.write(response.content)
#f1.close()

#print('output file: '  + os.path.realpath(f1.name))

f = io.BytesIO(response.content)
s3.meta.client.upload_fileobj(f, 'picamerastore', filename)

response.close()
