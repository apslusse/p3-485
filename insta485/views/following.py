"""
Insta485 following view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route('/u/<user_url_slug>/following/', methods=["GET", "POST"])
def show_following(user_url_slug):
    """Display / route."""
    # Get current user
    if "user" in flask.session:
        current = flask.session['user']
    else:
        return flask.redirect("/accounts/login/")

    # Connection to database
    connection = insta485.model.get_db()

    # Checking if user_url_slug exists in database
    cur = connection.execute(
        "SELECT 1 "
        "FROM users "
        "WHERE username = ?", (user_url_slug, )
    )
    exists = cur.fetchall()
    if not exists:
        flask.abort(404, description="User Not Found")
    else:
        pass

    page_u = user_url_slug

    # Connection to database
    connection = insta485.model.get_db()

    # Follow/Unfollow button
    if flask.request.method == 'POST':
        req = flask.request.form
        user = req['username']

        if 'follow' in req:
            connection.execute(
                "INSERT INTO following(username1, username2) "
                "VALUES (?, ?)", (current, user)
            )

        if 'unfollow' in req:
            connection.execute(
                "DELETE FROM following WHERE "
                "username1=? AND username2=?", (current, user)
            )

    # Querying all USERS that PAGE_USER follows...page_user->*USERS*
    cur = connection.execute(
        "SELECT u.username AS username, u.filename AS user_img_url "
        "FROM users u "
        "WHERE u.username IN ( "
        "SELECT username2 "
        "FROM following f "
        "WHERE f.username1 == ? )", (page_u,)
    )

    following = cur.fetchall()

    # Query to find all...current->*USERS*
    cur = connection.execute(
        "SELECT u.username AS username "
        "FROM users u "
        "WHERE u.username IN ( "
        "SELECT username2 "
        "FROM following f "
        "WHERE f.username1 == ? )", (current, )
    )
    curr_idols = cur.fetchall()

    # Checking if the users followed by page_user also followed by current
    # IF(page_user->user AND current->user) THEN true
    for people in following:
        # this condition is double checked
        if people['username'] == current:
            pass
        else:
            people['logname_follows_username'] = False
            for idol in curr_idols:
                if people['username'] == idol['username']:
                    people['logname_follows_username'] = True

    # Add database info to context
    context = {}
    context['user'] = user_url_slug
    context['logname'] = current
    context['following'] = following

    return flask.render_template("following.html", **context)
