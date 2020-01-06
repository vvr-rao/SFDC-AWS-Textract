import boto3
import io
from simple_salesforce import Salesforce
import requests
import os
from ftplib import FTP

s3 = boto3.resource('s3')

sf = Salesforce(username='<USERNAME>', password='<PASSWORD>', 
security_token='<TOKEN>', domain='test')

sessionId = sf.session_id
instance = sf.sf_instance

print ('sessionId: ' + sessionId)

#HARDCODED HERE FOR ILLUSTRATION
fileid = 'ID of Attachment'



attachment = sf.query("SELECT Id, Name, Body FROM Attachment where Id='" + fileid + 
"' LIMIT 1")
filename=attachment['records'][0]['Name']
print('filename: ' + filename)

response = requests.get('https://' + instance + 
'/services/data/v39.0/sobjects/Attachment/' + fileid + '/body',
headers = {  'Authorization': 'Bearer ' + sessionId })

#SAVE FILE LOCALLY
f1 = open(filename, "wb")
f1.write(response.content)

#upload to FTP
ftp = FTP('ftp site URL')
ftp.login(user='uname', passwd = 'password')

ftp.storbinary('STOR '+filename, open(filename, 'rb'))
ftp.quit()

f1.close()

print('output file: '  + os.path.realpath(f1.name))

#upload to S3
f = io.BytesIO(response.content)
s3.meta.client.upload_fileobj(f, 'BUCKET_NAME', filename)

response.close()

