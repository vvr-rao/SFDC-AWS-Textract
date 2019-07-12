let AWS = require('aws-sdk');
const textract = new AWS.Textract();

exports.handler = async (event,context,callback)  => {
        var inputVal = event.key;//SAMPLE INPUT - {   "key": "<filename>" }
        var params = {
                //ClientRequestToken: '1',
                DocumentLocation: { /* required */
                    S3Object: {
                    Bucket: 'BUCKET_NAME',
                    Name: inputVal
                    //Version: 'STRING_VALUE'
                    }
                },
                JobTag: 'SFDC',
                NotificationChannel: {
                    RoleArn: '<ROLE_ARN>', 
                    SNSTopicArn: '<SNS_TOPIC>' 
                }
        };

    textract.startDocumentTextDetection(params, function(err, data) {
        if (err) console.log(err, err.stack); // an error occurred
        else     console.log(data);           // successful response
    });

    callback(null, {"message": "Successfully executed"});
}
