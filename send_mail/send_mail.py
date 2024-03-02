import boto3
from botocore.exceptions import ClientError

SENDER = "YOUR EMAIL"
AWS_REGION = "ap-southeast-1"
SUBJECT = "CHECK IN SUCCESS"

def send_verify_checkin(email, url):
                
    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>CHECK IN STATUS</h1>
    <p> Check in success <p>
    <p>
    <a href='{url}'>image check in</a>
    </p>
    </body>
    </html>
                """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    email,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

if __name__ == "__main__":
    send_verify_checkin("tamlnhse@gmail.com", "abcc")
