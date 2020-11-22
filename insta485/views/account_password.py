"""
Insta485 accounts views.

URLs include:
/account/
"""
import uuid
import hashlib
import flask
import insta485


@insta485.app.route('/accounts/password/', methods=["GET", "POST"])
def show_acc_passwd():
    """Display modify password page."""
    # Get current user
    if "user" in flask.session:
        curr_user = flask.session['user']
    else:
        # If not logged in, redirect to login.
        return flask.redirect(flask.url_for('show_acclogin'))

    # Connect to database
    connection = insta485.model.get_db()

    if flask.request.method == 'POST':
        # Get form data
        req = flask.request.form
        old_password = req['password']
        new_password1 = req['new_password1']
        new_password2 = req['new_password2']

        # Fetch password for user
        cur = connection.execute(
            "SELECT username, password "
            "FROM users "
            "WHERE username = ? ",
            (curr_user,)
        )
        correct_login = cur.fetchall()

        # get database password and salt
        db_passwd_hash = correct_login[0]['password']
        db_passwd_salt = db_passwd_hash.split('$')
        db_passwd_salt = db_passwd_salt[1]

        # Hash the old password with same salt
        hash_passwod_input = password_db_string(old_password, db_passwd_salt)

        # See if hashed+salted is same as db hashed+salted for user
        if hash_passwod_input == db_passwd_hash:
            # Passwords match. Can change password

            # New passwords do not match. abort.
            if not new_password1 == new_password2:
                flask.abort(401)
            else:
                # New passwords match. Change password.
                new_password_hash = hash_password(new_password1)
                cur = connection.execute(
                    "UPDATE users "
                    "SET password = ? "
                    "WHERE username = ?",
                    (new_password_hash, curr_user)
                )

            return flask.redirect(flask.url_for('show_acc_edit'))

        # else: Old password does not match. abort.
        flask.abort(403)

    context = {}
    context["logname"] = curr_user
    return flask.render_template("/accounts/password.html", **context)


# Helper function. Returns salted hashed password matching database password.
def password_db_string(password, salt_input):
    """Return salted hashed password."""
    algorithm = 'sha512'
    salt = salt_input
    hash_obj = hashlib.new(algorithm)
    salted_password = salt + password
    hash_obj.update(salted_password.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    psswd_db_string = "$".join([algorithm, salt, password_hash])
    return psswd_db_string


# Helper function. Returns hash of password with random salt
def hash_password(password):
    """Return randomly salted hashed password."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    psswd_db_string = "$".join([algorithm, salt, password_hash])
    return psswd_db_string
