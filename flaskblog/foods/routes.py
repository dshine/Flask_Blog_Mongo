from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app)
from werkzeug.exceptions import default_exceptions
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import User
import requests

foods = Blueprint('foods', __name__)

@foods.route('/foods')
def list_foods():
    url = "https://www.themealdb.com/api/json/v1/1/categories.php"
    response = requests.request("GET", url)
    return render_template('foods.html', foods=response.json())


@foods.route("/foods/like/<fid>")
def like_movie(fid):
    user = User.objects(id=current_user.id)
    user.update(push__likes=fid)
    return "true"