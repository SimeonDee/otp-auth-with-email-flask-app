from . import oauth22 as oauth
import smtplib
import ssl
import base64
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import policy
from random import randint
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SENDER = getenv('MAIL_SENDER')
BASE_HOST = getenv('BASE_SERVER_HOST')

def get_auth_string():
    client_id = getenv('GOOGLE_CLIENT_ID')
    client_secret = getenv('GOOGLE_CLIENT_SECRET')
    refresh_token = getenv('REFRESH_TOKEN')

    # Generate new access token from refresh token
    token_response = oauth.RefreshToken(client_id, client_secret, refresh_token)
    access_token = token_response['access_token']

    # Generate Oauth2_String
    auth_string = oauth.GenerateOAuth2String(SENDER, access_token, base64_encode=False)

    return auth_string

def generate_otp_message(receiver, otp, type='html'):
    content = ''
    if type == 'html':
        content = f"""\
            <html>
                <body>
                    <h3>Verify Your OTP</h3>
                    <hr>
                    <div style="border: 1px solid gray; border-radius:10px; background-color: rgb(3, 3, 24); color: whitesmoke; padding: 5px 15px; font-size:2em; margin-top:10px; font-weight: 300; text-align:center">
                        <p>
                            Your OTP: {'-'.join(otp)}
                        </p>
                    </div>
                </body>
            </html>
        """
    else:
        content = f"""\
            Verify Your OTP
            ---------------

            Your OTP is {'-'.join(otp)}
        """
    message = MIMEText(content, 'html') if type=='html' else MIMEText(content, 'plain')
    message['From'] = SENDER
    message['To'] = receiver
    message['Subject'] = 'Verify OTP - Cornelius Auth App'

    return message

def send_otp_to_mail(receiver, otp, type='html'):
    try:
        OAUTH_STRING = get_auth_string()
        content_type = 'plain' if type != 'html' else type
        message = generate_otp_message(receiver, otp, type=content_type)

        with smtplib.SMTP_SSL('smtp.gmail.com', context=ssl.create_default_context()) as server:
            # server.set_debuglevel(True)
            server.ehlo('test')
            server.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(OAUTH_STRING.encode('utf-8')).decode('utf-8'))

            server.sendmail(SENDER, receiver, message.as_string())
            print('Message sent.')
            return {
                'success':True,
                'message':f'OTP Message sent to {receiver}.'
            }
    
    except Exception as ex:
        print(ex)
        return {
            'success':False,
            'message':f'Error sending OTP message, failed. Reason: {ex}'
        }


def generate_password_reset_message(receiver, target_route, type='html'):
    content = ''
    if type == 'html':
        content = f"""
            <html lang="en">
            <head></head>
            <body>
                <h3> Click the button below to reset your password </h3>
                <div>
                    <a href="{BASE_HOST}/{target_route}">
                        <button style="background-color: rgb(2, 6, 28); margin:5px; color:whitesmoke; font-size:1.2em; padding: 5px 10px; border-radius:3px">
                            Reset Password
                        </button>
                    </a>
                </div>
            </body>
            </html>
        """
    else:
        content = f"""\
            Hello,

            Click the link below to reset your password
            ---------------------------------------------

            "{BASE_HOST}/{target_route}"

        """


    message = MIMEText(content, 'html') if type=='html' else MIMEText(content, 'plain')
    message['From'] = SENDER
    message['To'] = receiver
    message['Subject'] = 'Reset Your Password - Cornelius Auth App'

    return message


def send_reset_link_to_mail(receiver, target_route, type='html'):
    try:
        OAUTH_STRING = get_auth_string()
        content_type = 'plain' if type != 'html' else type
        message = generate_password_reset_message(receiver, target_route, type=content_type)

        with smtplib.SMTP_SSL('smtp.gmail.com', context=ssl.create_default_context()) as server:
            # server.set_debuglevel(True)
            server.ehlo('test')
            server.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(OAUTH_STRING.encode('utf-8')).decode('utf-8'))

            server.sendmail(SENDER, receiver, message.as_string())
            print('Message sent.')
            return {
                'success':True,
                'message':f'Password reset link sent to {receiver}.'
            }
    
    except Exception as ex:
        print(ex)
        return {
            'success':False,
            'message':f'Error sending password reset link to email, failed. Reason: {ex}'
        }
    
# otp = str(randint(100000, 999999))
# receiver = 'adeyemi.sa1@gmail.com'

# response = send_otp_to_mail(receiver, otp, type='html')
# print(response)
