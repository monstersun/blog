from flask import Flask
from flask_mail import Message, Mail

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    MAIL_SERVER = 'smtp.126.com',
    MAIL_PORT = 25,
    MAIL_USERNAME = 'sxyzztx@126.com',
    MAIL_PASSWORD = 'sunaiding512',
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_DEBUG = True
)

mail = Mail(app)

app.route('/')
def index():
    msg = Message('Hi, this is a test mail', sender='sxyzztx@126.com', recipients=['sxyzztx@outlook.com'])
    msg.body = 'this is a test mail'
    mail.send(msg)
    print('mail sent')
    return 'sent'

if __name__ == '__main__':
    app.run()