"""
Insta485 user.

URLs include:
/u/<user_url_slug>/
/accounts/login/
"""
import pathlib
import uuid
import flask
import insta485

# last edit: Tues 10:30 ish


@insta485.app.route('/u/<user_url_slug>/', methods=["GET", "POST"])
def show_user(user_url_slug):
    """Display user page and manipulations."""
    # Get current user

    user = user_url_slug
    if "user" in flask.session:
        curr_user = flask.session['user']

    else:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()

    # Get form info
    req = flask.request.form
    # Connect to database
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT postid "
        "FROM posts "
    )

    posts = cur.fetchall()
    current_postid = len(posts)
    post_id = current_postid + 1

    if "user" in flask.session:
        curr_user = flask.session['user']

        # Get form info
        req = flask.request.form

        # Connect to database
        connection = insta485.model.get_db()

        if 'follow' in req:
            connection.execute(
                "INSERT INTO following(username1, username2)"
                "VALUES (?, ?)", (curr_user, user)
            )
        elif 'unfollow' in req:
            connection.execute(
                "DELETE FROM following WHERE "
                "username1=? AND username2=?", (curr_user, user)
            )

        elif 'create_post' in req:
            # Unpack flask object

            # filename = req["filename"]
            fileobj = flask.request.files["file"]
            filename = fileobj.filename

            # Compute base name (filename without directory).

            uuid_basename = "{stem}{suffix}".format(
                stem=uuid.uuid4().hex,
                suffix=pathlib.Path(filename).suffix
            )

            # Save to disk
            path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
            fileobj.save(path)

            connection.execute(
                "INSERT INTO posts(filename, owner)"
                "VALUES (?, ?);",
                (uuid_basename, curr_user)
            )
    # Query database

    # relationship to curr_user
    follows = False
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = '{}'".format(curr_user)
    )

    users_followed = cur.fetchall()
    # num_following = len(users_followed)

    for obj2 in users_followed:
        if obj2["username2"] == user:
            follows = True

    # Number of posts and post info, with correct English
    cur = connection.execute(
        "SELECT postid, filename AS img_url "
        "FROM posts "
        "WHERE owner = '{}'".format(user)
    )

    user_posts = cur.fetchall()

    for object in user_posts:
        object["img_url"] = "/uploads/" + object["img_url"]

    num_posts = len(user_posts)

    # number of followers
    cur = connection.execute(
        "SELECT username1 "
        "FROM following "
        "WHERE username2 = '{}'".format(user)
    )

    users_followers = cur.fetchall()
    num_followers = len(users_followers)

    # number of following
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = '{}'".format(user)
    )

    following = cur.fetchall()
    num_following = len(following)

    # name
    cur = connection.execute(
        "SELECT fullname "
        "FROM users "
        "WHERE username = '{}'".format(user)
    )

    name = cur.fetchall()
    name = name[0]["fullname"]

    # render
    context = {}
    context["logname"] = curr_user
    context["username"] = user
    context["logname_follows_username"] = follows
    context["posts"] = user_posts
    context["total_posts"] = num_posts
    context["following"] = num_following
    context["followers"] = num_followers
    context["fullname"] = name

    return flask.render_template("user.html", **context)
