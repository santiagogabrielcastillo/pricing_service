from flask import Blueprint, render_template, request, url_for, session
from werkzeug.utils import redirect

from models.alert import Alert
from models.item import Item
from models.store import Store
from models.user import requires_login

alert_bp = Blueprint('alerts', __name__)


@alert_bp.route('/')
@requires_login
def index():
    alerts = Alert.find_many_by('user_email', session['email'])
    return render_template('alerts/index.html', alerts=alerts)


@alert_bp.route('/new', methods=['GET', 'POST'])
@requires_login
def new_alert():
    if request.method == 'POST':
        alert_name = request.form['alert_name']
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])
        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)
        item.load_price()
        item.save_to_mongo()

        Alert(alert_name, item._id, price_limit, session['email']).save_to_mongo()
    return render_template('alerts/new_alert.html')


@alert_bp.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_mongo()
        return redirect(url_for('alerts.index'))
    return render_template('alerts/edit_alerts.html', alert=alert)


@alert_bp.route('/delete/<string:alert_id>')
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.remove_from_mongo()
    return redirect(url_for('alerts.index'))
