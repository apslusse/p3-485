"""
Insta485 accounts views.

URLs include:
/account/
"""
import hashlib
import flask
import insta485


@insta485.app.route('/accounts/login/', methods=["GET", "POST"])
def show_acclogin():
    """Account login."""
    # If already logged in, redirect to index
    if "user" in flask.session:
        return flask.redirect(flask.url_for('show_index'))

    # Connect to database
    connection = insta485.model.get_db()

    # Handle POST request
    if flask.request.method == 'POST':

        # Get form info
        req = flask.request.form
        plain_passwd_input = req['password']
        username_input = req['username']

        # Search for entries matching 'username_input'
        cur = connection.execute(
            "SELECT username, password "
            "FROM users "
            "WHERE username = ? ",
            (username_input,)
        )
        correct_login = cur.fetchall()

        if len(correct_login) == 0:
            # SQL Database query returned no results
            print("User does not exist")
            flask.abort(403)
        else:
            # Get password hash+salt of database
            db_passwd_hash = correct_login[0]['password']
            db_passwd_salt = db_passwd_hash.split('$')

            # Gets salt. [0] is hashing alg, [1] salt, [2] hashed password
            db_passwd_salt = db_passwd_salt[1]
            print("db_passwd_hash: " + db_passwd_hash)

            # Hash the login page password with same salt
            hash_passwod_input = password_db_string(plain_passwd_input,
                                                    db_passwd_salt)
            print("hash_passwod_input: " + hash_passwod_input)

            # See if hashed+salted is same as db hashed+salted for user
            if hash_passwod_input == db_passwd_hash:
                # Credentials match. Login!
                flask.session['user'] = username_input
                return flask.redirect(flask.url_for('show_index'))

            # else:
            flask.abort(403)

    context = {}
    return flask.render_template("/accounts/login.html", **context)


@insta485.app.route('/accounts/logout/', methods=["POST"])
def exec_logout():
    """Account logout."""
    flask.session.clear()
    return flask.redirect(flask.url_for('show_acclogin'))


# Helper function. Returns salted hashed password matching database password.
def password_db_string(password, salt_input):
    """Return salted hashed password matching database password."""
    algorithm = 'sha512'
    salt = salt_input
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    pss_db_string = "$".join([algorithm, salt, password_hash])
    return pss_db_string
