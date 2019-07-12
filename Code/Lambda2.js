let AWS = require('aws-sdk');

const s3 = new AWS.S3();
const textract = new AWS.Textract();

exports.handler = function(event, context, callback) {
    var message = event.Records[0].Sns.Message;
    var msgBody = JSON.parse(event.Records[0].Sns.Message);
    console.log('Message received from SNS:', message); 

    var JobId = msgBody.JobId;
    console.log(JobId); 

    var params = {
        JobId: JobId /* required */
        //MaxResults: 'NUMBER_VALUE',
        //NextToken: 'STRING_VALUE'
    };
    textract.getDocumentTextDetection(params, function(err, returnData) {
        console.log('function successfully called');
        if (err) console.log(err, err.stack); // an error occurred
        else     {
            //console.log(data);           // successful response

            let forUpload = '';

           console.log(returnData.Blocks.length);
           for(var index=0;index<returnData.Blocks.length;index++){
                //console.log(returnData.Blocks[index].BlockType);
                if(returnData.Blocks[index].BlockType == 'WORD'){//This code needs to be expanded to include PAGE, LINE etc.
                    //console.log(returnData.Blocks[index].Text);
                    forUpload = forUpload + '  ' + returnData.Blocks[index].Text;
                }
            }
           
            //console.log(forUpload);

            var params2 = {
                Bucket: "BUCKET_NAME", // name of dest bucket
                Key: 'FILE_NAME',
                Body: forUpload //'test string'//data
            };
            s3.upload(params2, function(err,data){
                if (err) console.log(err, err.stack);
                else console.log(data); 
            });
        }
    });

    callback(null, {"message": "Successfully executed"});
}
