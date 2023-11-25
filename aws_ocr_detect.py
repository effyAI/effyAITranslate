import boto3
import time
# from .upload_data import get_db
# Get AWS Credentials from MongoDB
# db = get_db()
# data = db['creds'].find_one()
# textract = boto3.client('textract', 'us-east-2', aws_access_key_id=data['aws_access_key_id'],
#                         aws_secret_access_key=data['aws_secret_access_key'])

aws_access_key_id = "AKIAVZBVXJWJLAWNRCWZ"
aws_secret_access_key="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"
region_name="us-east-1"

textract = boto3.client('textract', aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name)

s3BucketName = "effy-zero-shot"



def count_pages(document_name):
    objectName = document_name.strip()
    response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': objectName
            }
        })

    # 1st iteration of OCR from Textract
    response_1 = textract.get_document_text_detection(JobId=response["JobId"])
    status = response_1["JobStatus"]

    while status == "IN_PROGRESS":
        time.sleep(5)
        response_1 = textract.get_document_text_detection(JobId=response["JobId"])
        status = response_1["JobStatus"]
        print("Job status: {}".format(status))

    return response_1['DocumentMetadata']['Pages']


def startJob(objectName):
    # response = None
    objectName = objectName.strip()
    print("Object Name: ", objectName)
    response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': objectName
            }
        })

    return response["JobId"]


def isJobComplete(jobId):
    time.sleep(5)
    response = textract.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while status == "IN_PROGRESS":
        time.sleep(5)
        response = textract.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def getJobResults(jobId):
    pages = []

    time.sleep(5)
    response = textract.get_document_text_detection(JobId=jobId)

    pages.append(response)
    print("Result set page received: {}".format(len(pages)))
    nextToken = None
    if 'NextToken' in response:
        nextToken = response['NextToken']

    while nextToken:
        time.sleep(5)

        response = textract.get_document_text_detection(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        print("Result set page received: {}".format(len(pages)))
        nextToken = None
        if 'NextToken' in response:
            nextToken = response['NextToken']

    return pages


def textract_read(documentName, page):
    # Document
    pages = []
    s3 = boto3.resource('s3')
    jobId = startJob(documentName)
    print("Started job with id: {}".format(jobId))
    if isJobComplete(jobId):
        response = getJobResults(jobId)

    # Store Extracted Data in list
    print_list = []
    print_page = []
    page_check = 1
    # Print detected text

    if page == "All":
        for resultPage in response:
            for item in resultPage["Blocks"]:
                if item["BlockType"] == "PAGE":
                    if print_list:
                        print_page.append(print_list)
                        print_list = []
                        # print_list = ["Page " + str(item["Page"])]
                    # else:
                    #     print_list = ["Page 1"]

                if item["BlockType"] == "LINE":
                    print_list.append(item["Text"])

        # Append the last page
        if print_list:
            print_page.append(print_list)

    else:
        for resultPage in response:
            for item in resultPage["Blocks"]:
                if item["BlockType"] == "PAGE":
                    page_flag = item['Page']
                    if print_list:
                        print_page.append(print_list)
                        print_list = []

                if item["BlockType"] == "LINE" and page_flag==int(page):  # only when page is the same then store that
                    print_list.append(item["Text"])

        # Append Last Page
        if print_list:
            print_page.append(print_list)

    return print_page , response[0]['DocumentMetadata']['Pages']


# Function for PDF Files
def get_pdf_extracted(document_name, page):
    data_page = textract_read(document_name, page)
    return data_page


def detect_text(document_name):
    # Document
    documentName = document_name

    # Call Amazon Textract
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': documentName
            }
        })

    print_list = []
    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            # print('\033[94m' + item["Text"] + '\033[0m')
            print_list.append(item["Text"])

    return print_list


def get_docx_extracted(filename):
    return

if __name__ == "__main__":
    # print(detect_text('test.pdf'))
    print(textract_read(documentName="axis_1_en.pdf", page="All"))
