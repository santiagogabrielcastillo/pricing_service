from flask import Blueprint, render_template, request, url_for
import json

from werkzeug.utils import redirect
from models.user import requires_admin, requires_login
from models.store import Store

store_bp = Blueprint('stores', __name__)


@store_bp.route('/')
@requires_login 
def index():
    stores = Store.all()
    return render_template('stores/index.html', stores=stores)


@store_bp.route('/new', methods=['GET', 'POST'])
@requires_admin
def new_store():
    if request.method == 'POST':
        name = request.form['store_name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        Store(name, url_prefix, tag_name, query).save_to_mongo()
        return redirect(url_for('stores.index'))

    return render_template('stores/new_store.html')


@store_bp.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@requires_admin
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        name = request.form['store_name']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])
        store.name = name
        store.tag_name = tag_name
        store.query = query
        store.save_to_mongo()
        return redirect(url_for('stores.index'))
    return render_template('stores/edit_store.html', store=store)


@store_bp.route('/delete/<string:store_id>')
@requires_admin
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_mongo()
    return redirect(url_for('stores.index'))