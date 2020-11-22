"""
Insta485 accounts create.

URLs include:
/account/create/
/
"""
import uuid
import hashlib
import pathlib
import flask
import insta485

# last edit: monday 10:41


@insta485.app.route('/accounts/create/', methods=["GET", "POST"])
def show_acc_create():
    """Show page for create page and creates account for user."""
    # Get current user
    if "user" in flask.session:
        # curr_user = flask.session['user']
        return flask.redirect("/accounts/edit/")

    # Connect to database
    connection = insta485.model.get_db()

    success = False
    if flask.request.method == 'POST':
        # Handle post requests here.
        req = flask.request.form

        if req["username"] == "":
            flask.abort(409)

        if req["fullname"] == "":
            flask.abort(409)

        if req["email"] == "":
            flask.abort(409)

        # TODO: how to check for this
        # if req["file"] == "":
        #     flask.abort(409)

        fullname = req["fullname"]
        username = req["username"]
        # username already taken
        cur = connection.execute(
            "SELECT fullname "
            "FROM users "
            "WHERE username = '{}'".format(username)
        )

        user = cur.fetchall()
        # TODO : add for edge cases like theses
        if len(user) != 0:
            flask.abort(409)

        email = req["email"]

        # password

        # empty string for password
        if not req["password"]:
            flask.abort(400)

        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + req["password"]
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        password = password_db_string

        # profile pic

        fileobj = flask.request.files["file"]
        filename = fileobj.filename

        # Compute base name (filename without directory).
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            # Some comments...
            # Some comments...
            # Some comments...
            suffix=pathlib.Path(filename).suffix
        )

        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

        filename = uuid_basename

        # push to db
        connection.execute(
            "INSERT INTO users(username, fullname, email, filename, password)"
            "VALUES (?, ?, ?, ?, ?);",
            (username, fullname, email, filename, password)
        )
        success = True
        # successfully created, log user in and redirect
        flask.session['user'] = username

    if success:
        return flask.redirect("/")
    context = {}
    return flask.render_template("/accounts/create.html", **context)
