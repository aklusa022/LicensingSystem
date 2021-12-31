from flask import Flask

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp-relay.sendinblue.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'aklusa02@yandex.ru'
app.config['MAIL_PASSWORD'] = 'xsmtpsib-8030c7d67a90973584f9aebb47ac48fb8ca1fb691c302a2bfeb4e087447ed55d-wS2GvBpKtWbmA3zs'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.secret_key = "shhhhhh"