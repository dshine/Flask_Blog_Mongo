from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Language
from flaskblog.posts.forms import LangForm, PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    form.languages.choices = [(c.language.lower(), c.language) for c in Language.objects.order_by("language")]
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, 
            content=form.content.data, 
            user_id=current_user
        )
        post.address=form.address.data 
        post.loc = [float(form.lng.data), float(form.lat.data)]
        post.languages = form.languages.data
        post.save()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post',map_key=current_app.config["GOOGLE_MAPS_API_KEY"])

@posts.route("/post/map")
def post_map():
    posts = Post.objects.all()
    return render_template('map.html', posts=posts, map_key=current_app.config["GOOGLE_MAPS_API_KEY"])

@posts.route("/post/languages", methods=['GET', 'POST'])
def post_languages():
    form = LangForm()
    if form.validate_on_submit():
        lang = Language(
            language=form.language.data
        )
        lang.save()
        flash('You language has been saved', 'success')
        return redirect(url_for('posts.post_languages'))
    else:
        flash(f'Oh no, there was an error {form.errors}', 'success')
    return render_template('add_language.html', title="Add Language", form=form, legend="New Language")


@posts.route("/post/<post_id>")
def post(post_id):
    post = Post.objects.get_or_404(id=post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/lang/<search_language>")
@login_required
def language_search(search_language):
    posts = Post.objects(languages=search_language.lower()).order_by("-date_posted")
    #print(posts.user_id)
    return render_template('home.html', posts=posts)

@posts.route("/post/<post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.objects.get_or_404(id=post_id)
    if post.user_id.id != current_user.id:
        abort(403)
    form = PostForm()
    form.languages.choices = [(c.language.lower(), c.language) for c in Language.objects.order_by("language")]
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.address = form.address.data
        post.languages = form.languages.data
        post.loc = [float(form.lng.data), float(form.lat.data)]
        post.save()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.address.data = post.address
        form.languages.data = post.languages
        form.lng.data = post.loc['coordinates'][0] if post.loc != None else ''
        form.lat.data = post.loc['coordinates'][1] if post.loc != None else ''
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post',map_key=current_app.config["GOOGLE_MAPS_API_KEY"])


@posts.route("/post/<post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.objects.get_or_404(id=post_id)
    if post.user_id.id != current_user.id:
        abort(403)
    post.delete()
    #db.session.delete(post)
    #db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
