"""
Insta485 followers view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route('/u/<user_url_slug>/followers/', methods=["GET", "POST"])
def show_followers(user_url_slug):
    """Display / route."""
    # Get current user
    if "user" in flask.session:
        curr_user = flask.session['user']
    else:
        return flask.redirect(flask.url_for('show_acclogin'))

    # Connection to database
    connection = insta485.model.get_db()

    # Checking if user_url_slug exists in database
    yup = connection.execute(
        "SELECT 1 "
        "FROM users "
        "WHERE username = ?", (user_url_slug, )
    )
    exists = yup.fetchall()
    if not exists:
        flask.abort(404, description="User Not Found")
    else:
        pass

    # Get page user
    page_user = user_url_slug

    # Follow/Unfollow button
    if flask.request.method == 'POST':
        form = flask.request.form
        user = form['username']

        if 'follow' in form:
            connection.execute(
                "INSERT INTO following(username1, username2) "
                "VALUES (?, ?)", (curr_user, user)
            )

        if 'unfollow' in form:
            connection.execute(
                "DELETE FROM following WHERE "
                "username1=? AND username2=?", (curr_user, user)
            )

    # Querying for all users that follow page_user...*USERS*->page_user
    cur = connection.execute(
        "SELECT u.username, u.filename AS user_img_url "
        "FROM users u "
        "WHERE u.username IN ( "
        "SELECT f.username1 "
        "FROM following f "
        "WHERE f.username2 == ? )", (page_user, )
    )

    followers = cur.fetchall()

    # Querying for... curr_user->*USERS*
    cur = connection.execute(
        "SELECT username "
        "FROM users u "
        "WHERE u.username IN ( "
        "SELECT username2 "
        "FROM following f "
        "WHERE f.username1 == ? )", (curr_user, )
    )
    curr_idols = cur.fetchall()

    # checking if page_user followers are also followed by curr_user
    for follower in followers:
        # lol this condition is double checked (in HTML too) but whatever
        if follower['username'] == curr_user:
            pass
        else:
            follower['logname_follows_username'] = False
            for idol in curr_idols:
                if follower['username'] == idol['username']:
                    follower['logname_follows_username'] = True

    # Add database info to context
    context = {}
    context['user'] = user_url_slug
    context['logname'] = curr_user
    context['followers'] = followers

    return flask.render_template("followers.html", **context)
