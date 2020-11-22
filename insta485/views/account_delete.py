"""
Insta485 accounts views.

URLs include:
/account/
"""
import flask
import insta485


@insta485.app.route('/accounts/delete/', methods=["GET", "POST"])
def show_acc_delete():
    """Delete User Accounts."""
    # Get current user
    if "user" in flask.session:
        current = flask.session['user']
    else:
        # If not logged in, redirect to login.
        return flask.redirect(flask.url_for('show_acclogin'))

    # Connect to database
    connection = insta485.model.get_db()

    # Delete Account
    if flask.request.method == 'POST':
        req = flask.request.form
        if 'delete' in req:

            # deleting user icon from files
            cur = connection.execute(
                "SELECT filename "
                "FROM users "
                "WHERE username = ?", (current, )
            )
            u_pic = cur.fetchall()
            durl = insta485.app.config["UPLOAD_FOLDER"]/u_pic[0]['filename']
            durl.unlink()

            # delete user photos from files
            cur = connection.execute(
                "SELECT filename "
                "FROM posts p "
                "WHERE p.owner = ?", (current, )
            )
            post_urls = cur.fetchall()

            for val in post_urls:
                del_url = insta485.app.config["UPLOAD_FOLDER"]/val['filename']
                del_url.unlink()

            connection.execute(
                "DELETE FROM users WHERE "
                "username = ?", (current, )
            )
        flask.session.pop('user', None)
        return flask.redirect(flask.url_for('show_acc_create'))

    context = {}
    context['logname'] = current
    return flask.render_template("/accounts/delete.html", **context)
