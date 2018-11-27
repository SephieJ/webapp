# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, logout_user
from flask_wtf.csrf import CSRFProtect
from flask_menu import Menu
from app.src.users import services as user_services
from app.src.categories import services as category_services
from app.src.users.controllers import UserBP
from app.src.users.transactions.controllers import UserTransactionBP
from app.src.categories.controllers import CategoryBP
from app.src.faqs.controllers import FaqBP
from app.src.resources.controllers import ResourceBP
from app.src.users.supports.controllers import UserSupportBP
from app.src.company.controllers import CompanyBP
from app.src.utils import pusher_config, constants


app = Flask(__name__, template_folder='app/templates',
            static_folder='app/static')


# Secret key for CSRF token
app.config['SECRET_KEY'] = "\xe3X|L\xa5\x92\xfb~%*\x8e\xa3\xf5\ \
xab\t\x18\x12vY\xd7\x9at\xf8\x08"

# ReCaptcha Key
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeL9R8UAAAAAOEbwsvGS_e887ZlPGNLh2LaQoxR'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeL9R8UAAAAAHAQJ7w59FWGW5-kS4mbk\
SmFLYxh'

# Path to the upload dir ectory
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

# Allowed file extensions for image upload
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['TEMPLATES_AUTO_RELOAD'] = True

csrf = CSRFProtect(app)
Menu(app=app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'UserBP.login_page'
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    return user_services.get(int(user_id))


@app.context_processor
def fetch_categories():
    categories = category_services.get_categories()
    for category in categories:
        for subcategory in list(category['subcategories']):
            if subcategory['status'] != 'ACTIVE':
                category['subcategories'].remove(subcategory)
    return dict(categories=categories)


@app.context_processor
def fetch_user_favorites():
    user_favorites = []
    if current_user.is_authenticated:
        user_favorites = user_services.get_favorites(current_user.id)
    return dict(user_favorites=user_favorites)


@app.context_processor
def generate_pusher_app_key():
    pusher_app_key = pusher_config.app_key
    return dict(pusher_app_key=pusher_app_key)


@app.context_processor
def generate_base_url():
    base_url = constants.WEB_BASE_URL
    return dict(base_url=base_url)


@app.context_processor
def generate_one_map_url():
    one_map_url = constants.ONE_MAP_URL
    return dict(one_map_url=one_map_url)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_pages/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error_pages/500.html'), 500


@app.errorhandler(401)
def unauthorized(e):
    user_services.logout(current_user.id)
    logout_user()
    flash('You are not authorized for this transaction.', 'danger')
    return redirect(url_for('UserBP.login_page'))


app.register_blueprint(UserBP)
app.register_blueprint(UserTransactionBP)
app.register_blueprint(CategoryBP)
app.register_blueprint(FaqBP)
app.register_blueprint(ResourceBP)
app.register_blueprint(UserSupportBP)
app.register_blueprint(CompanyBP)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001, threaded=True)
