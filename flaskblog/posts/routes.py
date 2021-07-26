from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, 
            content=form.content.data, 
            user_id=current_user
        )
        post.address=form.address.data 
        post.loc['coordinates'][0]=form.lng.data
        post.loc['coordinates'][1]=form.lat.data
        post.save()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post',map_key=current_app.config["GOOGLE_MAPS_API_KEY"])


@posts.route("/post/<post_id>")
def post(post_id):
    post = Post.objects.get_or_404(id=post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.address = form.address.data
        post.loc['coordinates'][0] = form.lng.data
        post.loc['coordinates'][1] = form.lat.data
        post.save()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.address = post.address
        form.lng = post.loc['coordinates'][0]
        form.lat = post.loc['coordiantes'][1]
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
