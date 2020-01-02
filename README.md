# SFDC-AWS-Textract
Uses AWS Serverless components to expose Textract for use viaAPI Gaeway. Invoked from Salesforce using HTTP calls

This was a quick POC to show how to invoke the new AWS Textract Detect Text functionality from Salesforce. Utilized Serverless components extensively and exposed the functionality via API Gateway.

Solution has following components;
1) AN API Gateway endpoint which serves as a Proxy for S3. Instuctions to implement this are provided by AWS here:
  https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-s3.html. The only Addition I made was to allow the endpoint to accept Binary files
  'sendFile.txt' and 'sendAttachment.txt' - have sample Apex code of how you can send a File or Attachment from SFDC to API Gateway. I essentially retrieved the content of the Fil/Attachment as a blob and made a PUT request to my AWS endpoint.
2) A set of components to do a detect text in Textract. Used textract.startDocumentTextDetection and textract.getDocumentTextDetection since I needed to detect text in PDFs and they were the only functions with support that.

  The methods are asynchronous so I had to use the following pattern;

   'Lambda1.js' - this initates detect text using textract.startDocumentTextDetection. It is exposed the Salesforce via the API Gateway. Code is configured to create a message in an SNS topic on completion of a scan.

   'Lambda2.js' - this has been set as a Subscriber to the above SNS topic. Fires when a message is placed on SNS topic, retrives the text and places it on S3.
   
   'code to retrieve textract file from s3.txt' has sample Apex code to get the content back into Salesforce.

3) Also tested out zipping of files in S3 using JSZip.The following file has sample code - 'Zip-func.js'. Also exposed to Salesforce via API Gateway

EDIT: Jan 02, 2020. Was asked a question on whether it was posible to transfer files from Salesforce to AWS S3 without using the API Gateway. If you can host code, this is posible via Python. You will need to install the Simple_Salesforce and Boto3 libraries (Python SDKs for Salesforce and AWS), the following file has sample code on how to do this: 
## SFDC-To-AWS-S3.py  
