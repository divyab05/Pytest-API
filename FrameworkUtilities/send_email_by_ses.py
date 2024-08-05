import boto3, os
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from context import Context
#import pandas as pd
from email.mime.application import MIMEApplication

class Generate_Email_SES():



    def generate_email(self, text="", data=""):

        AWS_ACCESS_KEY = os.environ['AWS_KEY_ID']
        AWS_ACCESS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
        AWS_REGION = os.environ['AWS_REGION']
        recipients = os.environ['RECEIPIENTS']
        recipients = recipients.split(",")

        # Replace sender@example.com with your "From" address.
        # This address must be verified with Amazon SES.
        SENDER = os.environ['SENDER']

        # Replace recipient_list@example.com with a "To" address. If your account
        # is still in the sandbox, this address must be verified.
        #recipients = ["sachin.more@pb.com","anshul.gupta@pb.com"]
        #RECIPIENT = "sachin.more@pb.com"
        #RECIPIENT2 = "anshul.gupta@pb.com"

        #df = pd.read_csv("test_result.csv")




        # Specify a configuration set. If you do not want to use a configuration
        # set, comment the following variable, and the
        # ConfigurationSetName=CONFIGURATION_SET argument below.
        CONFIGURATION_SET = "ConfigSet"

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        # AWS_REGION = "us-west-2"

        BODY_TEXT = "Hello,\r\n" + "This is Test Email"

        # The subject line for the email.
        SUBJECT = "Shared Services API Automation Report : "+Context.ENV

        # The email body for recipients with non-HTML email clients.
        # The HTML body of the email.
        BODY_HTML = text

        textpart = data




        # The character encoding for the email.
        CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses', aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_ACCESS_SECRET_KEY,region_name=AWS_REGION)

        # Create a multipart/mixed parent container.
        msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        msg['Subject'] = SUBJECT
        msg['From'] = SENDER
        msg['To'] = ', '.join(recipients)

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart('alternative')
        '''
        def highlight_greaterthan_1(s):
            if s.Status == "PASS":
                return ['background-color: white'] * 8
            else:
                return ['background-color: red'] * 8

        df["Yesterday_count"] = pd.to_numeric(df["Yesterday_count"])
        df = df.style.apply(highlight_greaterthan_1, axis=1).set_properties(**{'text-align': 'center', 'border-color': 'Black', 'border-width': 'thin', 'border-style': 'dotted'})

        '''

        # Encode the text and HTML content and set the character encoding. This step is
        # necessary if you're sending a message with characters outside the ASCII range.
        #textportion = MIMEText(tabulate(data, headers="firstrow", tablefmt="grid").encode(CHARSET), 'plain', CHARSET)
        textportion = MIMEText(data)
        htmlpart = """    
        {0}
        """.format(data)


        
        #htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
        htmlpart = MIMEText(htmlpart, 'html')
        
        #text = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
        #html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))

        # Add the text and HTML parts to the child container.
        #msg_body.attach(textportion)
        msg_body.attach(htmlpart)

        # the attachment
        #part = MIMEApplication(open('D:/AUTOMATION/csd_monitoring_tool/test_result.csv', 'rb').read())
        #part.add_header('Content-Disposition', 'attachment', filename='test_result.csv')
        #msg.attach(part)

        # Define the attachment part and encode it using MIMEApplication.
        #att = MIMEApplication(open("htmlreport.html", 'rb').read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        #att.add_header('Content-Disposition', 'attachment', filename=os.path.basename("htmlreport.html"))

        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)

        # Add the attachment to the parent container.
        #msg.attach(att)
        # print(msg)
        try:
            # Provide the contents of the email.
            response = client.send_raw_email(
                Source=SENDER,
                Destinations=
                    recipients
                ,
                RawMessage={
                    'Data': msg.as_string(),
                },
                #ConfigurationSetName=CONFIGURATION_SET
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

if __name__=='__main__':
    print("Start of %s"%__file__)

    #Initialize the Email_Pytest_Report object
    email_obj = Generate_Email_SES()
    #1. Send html formatted email body message with pytest report as an attachment
    #Here log/pytest_report.html is a default file. To generate pytest_report.html file use following command to the test e.g. py.test --html = log/pytest_report.html
    email_obj.generate_email()