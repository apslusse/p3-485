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
    # Add database info to context
    context = {}
    context["logname"] = flask.session['user']

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
