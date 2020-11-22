"""
Insta485 explore view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route('/explore/', methods=["GET", "POST"])
def show_explore():
    """Display /explore route."""
    # Get current user
    if "user" in flask.session:
        curr_user = flask.session['user']
    else:
        # If not logged in, redirect to login.
        return flask.redirect(flask.url_for('show_acclogin'))

    if flask.request.method == 'POST':
        # Get form info
        # Connect to database
        connection = insta485.model.get_db()
        req = flask.request.form
        follow_user = req['username']

        # Add follow entry into database
        connection.execute(
            "INSERT INTO following(username1, username2) "
            "VALUES (?, ?);", (curr_user, follow_user)
        )

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ? ", (curr_user,)
    )
    following = cur.fetchall()

    # All usernames
    cur = connection.execute(
        "SELECT username, filename "
        "FROM users "
    )
    usernames = cur.fetchall()

    # Get list of people user is following
    following_list = []
    for followed in following:
        following_list.append(followed['username2'])

    # Get list of people user is not following and their profile picture
    not_following = []
    for user in usernames:
        not_followed = not user['username'] in following_list
        not_self = not user['username'] == curr_user
        if not_self and not_followed:
            not_following.append({'username': user['username'],
                                  'user_img_url': user['filename']})

    # Add database info to context
    context = {}
    context["logname"] = curr_user
    context["not_following"] = not_following

    return flask.render_template("explore.html", **context)
