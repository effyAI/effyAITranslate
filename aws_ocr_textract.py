import boto3
import time
import json

aws_access_key_id = "AKIAVZBVXJWJLAWNRCWZ"
aws_secret_access_key="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"
region_name="us-east-1"


textract = boto3.client('textract', aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name)
s3BucketName = "effy-zero-shot"
objectName = "axis_1_en.pdf"


def init_doc_analysis(bucket, document):
    response = textract.start_document_analysis(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket,
                'Name': document
            }
        },
        FeatureTypes=["TABLES", "FORMS"])

    job_id = response["JobId"]
    print("Started job with id: {}".format(job_id))
    return job_id

def get_anlysised_doc(job_id):
    response = textract.get_document_analysis(JobId=job_id)
    status = response["JobStatus"]
    while status == "IN_PROGRESS":
        time.sleep(5)
        response = textract.get_document_analysis(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))
    return response


if __name__ == "__main__":
    job_id = init_doc_analysis(s3BucketName, objectName)
    response = get_anlysised_doc(job_id)
    with open("test.json", "w") as f:
        json.dump(response, f)