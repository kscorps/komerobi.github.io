import os
from flask import Flask, render_template, redirect, url_for
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import Length, DataRequired, Email, NumberRange
from flask_wtf import FlaskForm
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USERNAME"] = os.environ.get('USER_EMAIL')
app.config["MAIL_PASSWORD"] = os.environ.get('USER_PASSWORD')
mail = Mail(app)

class MessageForm(FlaskForm):
    name = StringField(
        'Name:', [DataRequired(), Length(max=120)])
    email = StringField(
        'Email ID:', [Email(), Length(max=100)])
    phone = IntegerField(
        'Phone No:', [NumberRange(min=999999999, max=10000000000, message='Invalid Phone Number')])
    message = TextAreaField(
        'Message:', [Length(max=100)])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact_us', methods=['POST', 'GET'])
def contact_us():
    form = MessageForm()
    if form.validate_on_submit():
        name, email, message = (form.name.data, form.email.data, form.phone.data, form.message.data)
        msg = Message('', sender='komerobisalescorporation@gmail.com', recipients=['komerobisalescorporation@gmail.com'])
        msg.body = f'''
        New message recieved from your website:

        >>>Name: {name}
        >>>Email: {email}
        >>>Phone: {phone}
        >>>Message:
        {message}

        >>>Have a good day!
        '''
        mail.send(msg)
        return redirect(url_for('home'))
    return render_template('contact_us.html', form=form)

if __name__ == "__main__":
    app.run()