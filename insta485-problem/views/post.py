"""
Insta485 post.

URLs include:
/p/<curid>/
/accounts/login/
"""
import flask
import arrow
import insta485


# last edited: Mon 10 ish


@insta485.app.route('/p/<curid>/',  methods=["GET", "POST"])
def show_post(curid):
    """Display post and manipulation."""
    current_id = curid

    # Get current user
    if "user" in flask.session:
        curr_user = flask.session['user']

    else:
        return flask.redirect("/accounts/login/")

    # Connect to database
    connection = insta485.model.get_db()

    # Handle POST if it is POST
    if flask.request.method == 'POST':
        # Get form info
        req = flask.request.form
        # Connect to database
        connection = insta485.model.get_db()

        if 'unlike' in req:
            connection.execute(
                "DELETE FROM likes WHERE "
                "owner=? AND postid=?", (curr_user, current_id)
            )
        elif 'like' in req:
            connection.execute(
                "INSERT INTO likes(owner, postid)"
                "VALUES (?, ?)", (curr_user, current_id)
            )

        elif 'comment' in req:
            comment = req['text']
            connection.execute(
                "INSERT INTO comments(owner, postid, text)"
                "VALUES (?, ?, ?);",
                (curr_user, current_id, comment)

            )

        elif 'uncomment' in req:
            deleteid = req['commentid']

            cur = connection.execute(
                "SELECT owner "
                "FROM comments "
                "WHERE commentid = " + deleteid
            )

            owner_like = cur.fetchall()

            # TODO: what to do if post does not exist
            if owner_like[0]["owner"] != curr_user:
                flask.abort(403)

            connection.execute(
                "DELETE FROM comments WHERE "
                "owner=? AND postid=? AND commentid=?",
                (curr_user, current_id, deleteid)
            )

        elif 'delete' in req:

            # deleteid = req['postid']
            postid_delete = req['postid']

            cur = connection.execute(
                "SELECT owner "
                "FROM posts "
                "WHERE postid = " + postid_delete
            )

            owner_post = cur.fetchall()

            if len(owner_post) == 0:
                flask.abort(404)

            if owner_post[0]["owner"] != curr_user:
                flask.abort(403)

            cur = connection.execute(
                "SELECT filename "
                "FROM posts "
                "WHERE postid = " + postid_delete
            )

            filename_post = cur.fetchall()

            connection.execute(
                "DELETE FROM comments WHERE "
                "postid=?", [postid_delete]
            )

            connection.execute(
                "DELETE FROM likes WHERE "
                "postid=?", [postid_delete]
            )

            connection.execute(
                "DELETE FROM posts WHERE "
                "postid=?", [postid_delete]
            )

            fname_del = filename_post[0]['filename']
            delete_url = insta485.app.config["UPLOAD_FOLDER"]/fname_del
            delete_url.unlink()
            return flask.redirect("/u/{}/".format(owner_post[0]["owner"]))

    # Query database
    # info from post table
    cur = connection.execute(
        "SELECT filename, owner, created "
        "FROM posts "
        "WHERE postid = " + current_id
    )

    post = cur.fetchall()
    # TODO : add for edge cases like theses
    if len(post) == 0:
        flask.abort(404)

    post = post[0]

    timestamp = arrow.get(post["created"], 'YYYY-MM-DD HH:mm:ss').humanize()

    # likes
    cur = connection.execute(
        "SELECT owner "
        "FROM likes "
        "WHERE postid = " + current_id
    )

    likes = cur.fetchall()

    # TODO: test
    like_status = False
    for obj in likes:
        if obj["owner"] == curr_user:
            like_status = True

    # comments
    cur = connection.execute(
        "SELECT commentid, owner, text "
        "FROM comments "
        "WHERE postid = " + current_id
    )

    comments = cur.fetchall()

    # users
    post_owner = post["owner"]
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = '{}'".format(post_owner)
    )

    profile_pic = cur.fetchall()
    profile_pic = profile_pic[0]["filename"]

    # render
    context = {}
    context["logname"] = curr_user
    # info from post table
    context["postid"] = current_id
    context["img_url"] = "/uploads/" + post["filename"]
    context["owner_img_url"] = "/uploads/" + profile_pic
    context["owner"] = post["owner"]
    context["timestamp"] = timestamp
    # info from likes
    context["likes"] = len(likes)
    # info from comments

    context["comments"] = comments
    context["like_status"] = like_status

    return flask.render_template("post.html", **context)
