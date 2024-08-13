from setup import create_app
from db import db
from flask import (
    request, render_template, 
    jsonify, url_for, make_response,
    redirect, session
    )
from models import User, create_db_tables
from utils.sendmail import (send_otp_to_mail, 
                            send_reset_link_to_mail)
from utils.utilities import (
    create_otp, date_diff_in_secs)
from datetime import datetime, timezone

OTP_MAXIMUM_LIFE_IN_SECS = 60 * 2 # 2 minutes

app = create_app()
# Create DB Tables
# create_db_tables(app)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        if 'user' in session:
            user = session['user']
            username = user['fullname']

            all_users = User.query.all()
            return render_template('index.html', username=username, users=all_users)
        else:
            return redirect(url_for('login'))

    else:
        err_msg = 'Invalid Method Call'
        return render_template('error_page.html', error_message=err_msg)


############
# REGISTER
############
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        # collect user data
        data = request.form if request.form else request.json 

        try:
            if ('matric' not in data or 'email' not in data or
                'password' not in data or 'fullname' not in data):
                
                raise Exception('"matric", "email", "password" and "fullname" fields are required fields.')
           
            # create new user from collected data
            new_user = User(**data) 

            # Add the new user to db
            db.session.add(new_user)
            db.session.commit()

            # return jsonify({
            #     "success": True,
            #     'user': new_user.to_json()
            # })
            return render_template('register_success.html', username=new_user.fullname)
        
        except Exception as ex:
            return render_template('register.html', error_message=ex.__str__(), form_data=data)


##########
# LOGIN
##########
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user' in session:
            return render_template('index.html', user=session['user'])
        
        return render_template('login.html')
    
    elif request.method == 'POST':
        # collect user data
        data = request.form if request.form else request.json 

        try:
            if 'email' not in data or 'password' not in data:
                raise Exception('"email" and "password" fields are required in post data.')

            email = data['email']
            password = data['password']

            # Authenticate user from collected data
            user = User.query.filter_by(email=email, password=password).first()

            if user:
                user.password = ''
                session['user'] = user.to_json()
                return redirect(url_for('generate_otp'))
            else:
                return render_template('login.html', error_message="Invalid login credentials", email=email, password=password)
        
        except Exception as ex:
            return render_template('login.html', error_message=ex, email=email, password=password)
            
###################
# GENERATE OTP
###################

@app.route('/generate_otp', methods=['GET'])
def generate_otp():
    if request.method == 'GET':
        if 'user' not in session:
            return redirect(url_for('login'))
        
        request_otp = request.args.get('fetchotp', None)
        if request_otp is None:
            return render_template('otp.html')
        else:
            receiver_email = session['user']['email']
            otp = create_otp(size=6)
            response = send_otp_to_mail(receiver_email, otp, type='html')

            if response['success'] == True:
                session['otp_created_at'] = datetime.now()
                session['otp'] = otp

            return render_template('otp.html', response=response, otp_duration=OTP_MAXIMUM_LIFE_IN_SECS)
    return render_template('error_page.html', error_message='Invalid method call')
           
###################
# VERIFY OTP
###################

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        if 'user' not in session:
            return redirect(url_for('login'))
        
        data = request.form if request.form else request.json
        if 'otp-input' not in data:
            return render_template('otp.html', error_message='otp-input field is required to be filled.')

        if 'user' in session and 'otp' in session and 'otp_created_at' in session:
            created_at = session['otp_created_at'].replace(tzinfo=None)
            used_at = datetime.now().replace(tzinfo=None)

            print(f'Old Datetz:\n{created_at}')
            print(f'New Daterm:\n{used_at}')

            input_token = data['otp-input']
            expired = True if (date_diff_in_secs(used_at, created_at) > OTP_MAXIMUM_LIFE_IN_SECS) else False

            if session['otp'] != input_token:
                return render_template('otp.html', error_message='OTP-input token is Invalid. Kindly re-check your mail again.')
            elif session['otp'] == input_token and expired:
                return render_template('otp.html', error_message='OTP-input token has expired. Kindly generate a new one.')
            elif session['otp'] == input_token and expired == False:
                return redirect(url_for('index'))



###################
# FORGOT PASSWORD
###################
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    elif request.method == 'POST':
        data = request.form if request.form else request.json

        if 'email' not in data:
            raise Exception('"email" field is required in post data.')

        # TODO: send link for user to change password to email
        user = User.query.filter_by(email=data['email']).first_or_404()
        if user:
            id = user.id
            route_link = f'/reset_password/{id}'
            response = send_reset_link_to_mail(
                receiver=user.email, target_route=route_link, type='html')
            
            return render_template('forgot_password_mail_sent_confirm.html',
                                response=response)
        else:
            return render_template('forgot_password.html', email=data['email'], 
                                   error_message='No such email existing in our records.')



@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id, f'User with id {id}, not found.')

    if request.method == 'GET':
        return render_template('update_user.html', user=user)
    elif request.method == 'POST':
        data = request.form if request.form else request.json

        user.matric = data['matric']
        user.email = data['email']
        user.fullname = data['fullname']

        db.session.commit()

        return redirect(url_for('index'))
    
@app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    
    if request.method == 'GET':
        user = User.query.get_or_404(id, f'User with id {id}, not found.')
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('error_page.html', error_message="Invalid method call on delete user")


@app.route('/reset_password/<int:id>', methods=['GET', 'POST'])
def reset_password(id):
    if request.method == 'GET':
        user = User.query.get_or_404(id, 'User not found, Or link has been tampered with')       
        return render_template('reset_password.html', username=user.fullname, user_id=user.id)
    elif request.method == 'POST':
        data = request.form if request.form else request.json
        if 'new_password' not in data:
            return render_template(
                'reset_password.html', username=user.fullname, 
                user_id=id, error_message='The new-password field is required')
        
        new_password = data['new_password']
        
        user = User.query.get_or_404(id, 'User not found, Or link has been tampered with')
        user.password = new_password

        db.session.commit()

        return render_template('password_reset_success.html', username=user.fullname)



            
    


########################
    # ADMIN
########################
@app.route('/admin', methods=['GET'])
def admin_index():
    if request.method == 'GET':
        all_users = User.query.all()
        return render_template('admin.html', username='Super User', users=all_users)
    else:
        err_msg = 'Invalid Method Call'
        return render_template('error_page.html', error_message=err_msg)


########################
    # LOGOUT
########################
@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))



#######################
# ERROR HANDLERS
#######################
@app.errorhandler(404)
def error_404(error):
    return render_template('error_page.html', error_message=error)

@app.errorhandler(500)
def error_500(error):
    return render_template('error_page.html', error_message=error)

# Default exceptions
@app.errorhandler(Exception)
def uncaught_exceptions(error):
    return render_template('error_page.html', error_message=error)
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)