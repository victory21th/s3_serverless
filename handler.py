import boto3
import logging
import os

s3_client = boto3.client('s3')

logging.basicConfig()
logger = logging.getLogger('s3_handler')
logger.setLevel(logging.INFO)


def main(event, context):
    """
    Triggered by s3 events, object create
    """
    # Sample event:
    #
    # _event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1',
    # 'eventTime': '2019-09-27T19:10:14.822Z', 'eventName': 'ObjectCreated:Put',
    # 'userIdentity': {'principalId': 'A2DRN2TSDZDW7S'}, 'requestParameters': {'sourceIPAddress': '45.62.42.9'},
    # 'responseElements': {'x-amz-request-id': '52AC9DA8F64D8AF1', 'x-amz-id-2': 'vN8oJomSFEvXAkaESHHqD1EgK4PIu36KSIIUxgmoE+4kdpAZ5NqWxCd1Oi1pLLAxSIT5Agl4mI8='},
    # 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'f32b804e-ffe0-4a6b-a838-4fc32b102182',
    # 'bucket': {'name': 'rennantest123', 'ownerIdentity': {'principalId': 'A2DRN2TSDZDW7S'}, 'arn': 'arn:aws:s3:::rennantest123'},
    # 'object': {'key': 'Incoming/test.txt', 'size': 77, 'eTag': 'b3c5f33e9d7f3447da289f0920c9d550', 'sequencer': '005D8E5E96C64DE262'}}}]}
    try:
        logger.info('------------------')
        logger.info('start handler')
        logger.info('event: {}'.format(event))

        bucket_name = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        file_name = key.replace('{}/'.format(os.environ['S3_KEY_BASE']), '')
        file_size = event['Records'][0]['s3']['object']['size']

        if (bucket_name == os.environ['S3_BUCKET_NAME'] and file_name != '' and file_size > 0):
            # Print content
            response = s3_client.get_object(Bucket=os.environ['S3_BUCKET_NAME'], Key=key)
            file_content = response['Body'].read().decode('utf-8')
            logger.info('file_content: {}'.format(file_content))

            # Move file
            s3_client.copy_object(Bucket=os.environ['S3_BUCKET_NAME'],
                                  CopySource={'Bucket': os.environ['S3_BUCKET_NAME'], 'Key': key},
                                  Key="{}/{}".format(os.environ['S3_NEW_KEY_BASE'], file_name))
            s3_client.delete_object(Bucket=os.environ['S3_BUCKET_NAME'], Key=key)

        else:
            logger.error("Invalid input")
            return {
                "status": "fail"
            }
    except Exception as e:
        logger.error(e)
        return {
            "status": "fail"
        }
    return {
        "status": "success"
    }


if __name__ == "__main__":
    main({'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1',
                       'eventTime': '2019-09-27T20:07:08.067Z', 'eventName': 'ObjectCreated:Put',
                       'userIdentity': {'principalId': 'A2DRN2TSDZDW7S'},
                       'requestParameters': {'sourceIPAddress': '45.62.42.9'},
                       'responseElements': {'x-amz-request-id': 'A02AACCB8F19C29B',
                                            'x-amz-id-2': '7qagETWTexB4cE10BqHs7K/m4uD23fgL2wj7Z7IWFk9o9iwvj0MpLtS8RK+ICNb5JqjNT1GZBhc='},
                       's3': {'s3SchemaVersion': '1.0', 'configurationId': '0adb7e30-8e98-4ea9-b426-6b7356ef8214',
                              'bucket': {'name': 'rennantest123', 'ownerIdentity': {'principalId': 'A2DRN2TSDZDW7S'},
                                         'arn': 'arn:aws:s3:::rennantest123'},
                              'object': {'key': 'Incoming/test.txt', 'size': 77,
                                         'eTag': 'b3c5f33e9d7f3447da289f0920c9d550',
                                         'sequencer': '005D8E6BEC0106203A'}}}]}, None)
