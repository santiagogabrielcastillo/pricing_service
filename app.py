import os
from flask import Flask, render_template
from views.users import users_bp
from views.alerts import alert_bp
from views.stores import store_bp


app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)
print('')
@app.route('/')
def home():
    return render_template('home.html')

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(alert_bp, url_prefix="/alerts")
app.register_blueprint(store_bp, url_prefix="/stores")


if __name__ == '__main__':
    app.run(debug=True)