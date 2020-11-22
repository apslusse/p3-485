"""
Insta485 accounts views.

URLs include:
/account/
"""
import pathlib
import uuid
import flask
import insta485


@insta485.app.route('/accounts/edit/', methods=["GET", "POST"])
def show_acc_edit():
    """Edit Accounts. Changes entries in database."""
    # Get current user
    if "user" in flask.session:
        curr_u = flask.session['user']
    else:
        # If not logged in, redirect.
        return flask.redirect(flask.url_for('show_acclogin'))

    # Connect to database
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT fullname, email, filename "
        "FROM users u "
        "WHERE u.username = ?", (curr_u, )
    )
    user_info = cur.fetchall()
    user_pic = user_info[0]['filename']
    # Fetch Data

    if flask.request.method == 'POST':
        req = flask.request.form
        fileobj = flask.request.files["file"]
        filename = fileobj.filename

        if 'update' in req:
            name = req['fullname']
            email = req['email']

            if filename != "":
                uuid_basename = "{stem}{suffix}".format(
                    # Some comments...
                    stem=uuid.uuid4().hex,
                    # Some comments...
                    # Some comments...
                    # Some comments...
                    suffix=pathlib.Path(filename).suffix
                    # Some comments...
                    # Some comments...
                    # Some comments...
                )
                path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
                fileobj.save(path)
                url = insta485.app.config["UPLOAD_FOLDER"]/user_pic
                url.unlink()

                connection.execute(
                    "UPDATE users "
                    "SET filename = ? "
                    "WHERE username = ?", (uuid_basename, curr_u)
                )
            connection.execute(
                "UPDATE users "
                "SET fullname = ?, email = ? "
                "WHERE username = ?", (name, email, curr_u)
            )
            cur = connection.execute(
                "SELECT fullname, email, filename "
                "FROM users u "
                "WHERE u.username = ?", (curr_u, )
            )
            updated_info = cur.fetchall()
            context = {}
            context['logname'] = curr_u
            context['fullname'] = updated_info[0]['fullname']
            context['email'] = updated_info[0]['email']
            context['filename'] = updated_info[0]['filename']

            return flask.render_template("/accounts/edit.html", **context)

    context = {}
    context['logname'] = curr_u
    context['fullname'] = user_info[0]['fullname']
    context['email'] = user_info[0]['email']
    context['filename'] = user_info[0]['filename']
    return flask.render_template("/accounts/edit.html", **context)
