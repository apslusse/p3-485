"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485


@insta485.app.route('/', methods=["GET", "POST"])
def show_index():
    """Display / route."""
    # Get current user
    if "user" in flask.session:
        curr_user = flask.session['user']
    else:
        # If not logged in, redirect to login.
        return flask.redirect(flask.url_for('show_acclogin'))

    # Handle POST if it is POST
    if flask.request.method == 'POST':
        if 'unlike' in flask.request.form:
            insta485.model.get_db().execute(
                "DELETE FROM likes WHERE "
                "owner=? AND postid=?",
                (curr_user, flask.request.form['postid'])
            )
        elif 'like' in flask.request.form:
            insta485.model.get_db().execute(
                "INSERT INTO likes(owner, postid)"
                "VALUES (?, ?)",
                (curr_user, flask.request.form['postid'])
            )
        elif 'comment' in flask.request.form:
            comment = flask.request.form['text']
            insta485.model.get_db().execute(
                "INSERT INTO comments(owner, postid, text)"
                "VALUES (?, ?, ?);",
                (curr_user, flask.request.form['postid'], comment)
            )

    # Fetch posts of user following current user
    cur = insta485.model.get_db().execute(
        "SELECT "
        "posts.postid, "
        "posts.filename AS postimage, "
        "posts.owner, posts.created, "
        "following.username2, "
        "following.username1 "
        "FROM posts "
        "INNER JOIN following AS userfollow ON following.username1=? "
        "INNER JOIN following ON following.username2=posts.owner "
        "GROUP BY posts.postid "
        "ORDER BY posts.postid DESC", (curr_user,)
    )
    posts = cur.fetchall()

    # Fetch users own posts
    cur = insta485.model.get_db().execute(
        "SELECT postid, filename AS postimage, owner, created "
        "FROM posts "
        "WHERE owner=?", (curr_user,)
    )
    profile_pic = cur.fetchall()

    # Append profile_pic (self_posts) to posts. Style workaround.
    posts = profile_pic + posts

    # Sort new posts by postid.
    posts.sort(key=lambda x: x['postid'])

    # Fetch data for profile picture
    cur = insta485.model.get_db().execute(
        "SELECT username, filename "
        "FROM users"
    )
    profile_pic = cur.fetchall()

    # Fetch likes
    cur = insta485.model.get_db().execute(
        "SELECT postid, owner "
        "FROM likes"
    )
    likes = cur.fetchall()

    # Fetch comment data
    cur = insta485.model.get_db().execute(
        "SELECT commentid, owner, postid, text "
        "FROM comments "
        "ORDER BY commentid"
    )
    comments = cur.fetchall()  # collection of comments each with metadata.

    # Fetch largest postid value
    cur = insta485.model.get_db().execute(
        "SELECT MAX(postid)"
        "FROM posts "
    )
    maxpostid = cur.fetchall()
    maxpostid = maxpostid[0]['MAX(postid)']
    maxpostid += 1

    # Initialize like info
    like_status = [False] * maxpostid  # index is postid, value is like status
    like_count = [0] * maxpostid  # index is postid, value is like count.
    for like_obj in likes:  # like_obj:{postid : x} x likes for post
        # Count likes for each post
        like_count[like_obj['postid']] += 1

        # Identify like status for each post
        if like_obj['owner'] == curr_user:
            like_status[like_obj['postid']] = True

    # Aggregate comments with same postid to one list
    # Initialize all_comment: list of list of comment for each post.
    all_comment = [[] for i in range(maxpostid)]

    for comment in comments:
        # add comment to post.
        all_comment[comment['postid']].append(comment)

    # Add all data (like_num, like_status, userpic) to posts
    for post in posts:
        # Add like count info to posts
        post["like_num"] = like_count[post['postid']]

        # Add like status info to posts
        post["like_status"] = like_status[post['postid']]

        # Add profile picture data to each post
        for pic_data in profile_pic:
            if pic_data['username'] == post['owner']:
                post['userimage'] = '/uploads/' + pic_data['filename']

        # Reformat post link
        post['postimage'] = '/uploads/' + post['postimage']

        # Reformat date data
        post["created"] = arrow.get(post["created"], 'YYYY-MM-DD HH:mm:ss')
        post["created"] = post["created"].humanize()

        # Add comments to posts
        post["comments"] = all_comment[post['postid']]

    # Add database info to context
    context = {}
    context["logname"] = curr_user
    context["posts"] = posts
    return flask.render_template("index.html", **context)


@insta485.app.route('/css/style.css')
def serve_css():
    """Serve css when requested."""
    return flask.send_from_directory('/static/css/', '/static/css/style.css')


@insta485.app.route('/uploads/<path:imagename>')
def serve_image(imagename):
    """Serve image when requested."""
    # Check if logged in
    if "user" in flask.session:
        return flask.send_from_directory(insta485.config.UPLOAD_FOLDER,
                                         imagename)

    # If not logged in, abort(403) per spec
    flask.abort(403)
    return None
