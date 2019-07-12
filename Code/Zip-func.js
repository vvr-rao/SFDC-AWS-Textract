var JSZip = require("jszip");
let AWS = require('aws-sdk');

const zip = new JSZip();
const s3 = new AWS.S3();

exports.handler = async (event)  => {
       
    var inputVal = event.key; //SAMPLE INPUT - {   "key": "<file1>,<file2>,<file3>" }
    var FileList = inputVal.split(',');
    var arrayLength = FileList.length;
    
    for (var i = 0; i < arrayLength; i++) {
        console.log(FileList[i]);
        var params = {
            Bucket: "BUCKET_NAME",
            Key: FileList[i]
        };

    let inputData = await s3.getObject(params).promise();

    zip.file(FileList[i], inputData.Body);
    }
    
    var content = zip.generateNodeStream({
            type: 'nodebuffer',
            streamFiles:true
        });

    console.log('Came here');
    
    var params2 = {
            Bucket: "BUCKETNAME", // name of dest bucket
            Key: 'FILE TO STORE THE ZIP',
            Body: content,
            ACL: 'public-read'//NOTE: created this to make the zip file public. remove if you would rather it be private
    };

    

    await s3.upload(params2).promise();

}
