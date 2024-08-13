from os import getenv
from flask_mail import Message
from .mailer import mail

# host = getenv('MAIL_SERVER')
# port = getenv('MAIL_PORT')
# sender = getenv('MAIL_SENDER')

# password = getenv('MAIL_PASSWORD')
# server = SMTP(host, port)

base_host = getenv('BASE_SERVER_HOST')

def send_mail(receiver, target_route, type='html'):
    content = f"""
        <html lang="en">
        <head></head>
        <body>
            <h3> Click the button below to reset your password </h3>
            <a href="{base_host}{target_route}">
                <button style="background-color: rgb(2, 6, 28); color:whitesmoke; padding: 5px 10px; border-radius:3px">
                    Reset Password
                </button>
            </a>
        </body>
        </html>
    """
    try:
        message = Message()
        message.subject = 'Reset Password'
        message.recipients = [receiver]
        message.html = content

        mail.send(message)
        return {'success':True, 'message': 'Mail Sent'}
    except Exception as error:
        return {'success':False, 'message': error}



