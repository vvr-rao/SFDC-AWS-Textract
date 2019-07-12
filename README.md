# SFDC-AWS-Textract
Uses AWS Serverless components to expose Textract for use. Invoked from Salesforce using HTTP calls

This was a quick POC to show how to invoke the new AWS Textract functionality from Salesforce. Utilized Serverless components extensively and exposed the functionality via API Gateway.

Solution has following components;
1) an API Gateway to S3 which serves as a Proxy. Instuctions to implement this are provided by AWS here:
  https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-s3.html
  Files - sendFile.txt and sendAttachment.txt - have sample code of how you can send a File or Attachment from SFDC to API Gateway
2) set of components to do a detect text in Textract. Used textract.startDocumentTextDetection and textract.getDocumentTextDetection since I needed to detect text in PDFs and they were the only functions with support that.

  The methods are asynchronous so I had to use the following pattern;

   Lambda1.py - this initates detect text using textract.startDocumentTextDetection. It is exposed the Salesforce via the API Gateway. Code is configured to create a message in an SNS topic on completion of a scan.

   Lambda2.py - this has been set as a Subscriber to the above SNS topic. Fires when a message is placed on SNS topic

3) Also tested out zipping of files in S3. Follow file has sample code - Zip-func.py. Also exposed to Salesforce via API Gateway
