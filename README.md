# otp-auth-with-email-flask-app

# About
This project implements a simple authentication system with email-based OTP (One Time Password) feature and Oauth2 authentication to mail server. 

---

1. Features
   - Authentication
   - Timer-based OTP (One Time Password)
   - Google Oauth2 Authentication (for mail server authorization)
   - Database operations with SQLAlchemy
   - Cross-Origin Request Management
   - Templating Engine (Jinja2)
   - Session Management
   - Token generation (random.randint)
    
3. Tools
   - Flask
   - flask-SQLAlchemy
   - Jinja2
   - smtplib and email (for email server connectivity and messaging)
   - oauth2
   - base64(for convertion of oauth string)
   - flask-CORS
   - dotenv and os (Environment variable management)
   - datetime (for token expiry timer implementation)

# Installations and Setup
- Installing dependencies


`
$ pip install -r requirements.txt
`

- Running the server locally
  
`
$ python ./app.py
`
