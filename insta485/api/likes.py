"""REST API for likes."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/',
                    methods=["GET", "DELETE", "POST"])
def get_likes(postid_url_slug):
    """Use to return number of likes given post id."""
    if "user" in flask.session:
        if flask.request.method == 'DELETE':
            cur = insta485.model.get_db().execute(
                "DELETE FROM likes "
                "WHERE postid=? AND owner=?",
                (postid_url_slug, flask.session['user'])
            )
            return flask.make_response("", 204)
        elif flask.request.method == 'GET':
            cur = insta485.model.get_db().execute(
                "SELECT * "
                "FROM likes WHERE postid=? ",
                (postid_url_slug,)
            )
            likes = cur.fetchall()
            number_of_likes = len(likes)
            logname_likes = 0
            for like in likes:
                if like['owner'] == flask.session['user']:
                    logname_likes = 1

            context = {
                "logname_likes_this": logname_likes,
                "likes_count": number_of_likes,
                "postid": postid_url_slug,
                "url": flask.request.path,
            }
            return flask.jsonify(**context)
        elif flask.request.method == 'POST':
            cur = insta485.model.get_db().execute(
                "INSERT OR IGNORE INTO likes "
                "(owner, postid) VALUES (?,?)",
                (flask.session['user'], postid_url_slug)
            )

            if cur.lastrowid != 0:
                context = {
                    "logname": flask.session['user'],
                    "postid": postid_url_slug
                }
                return flask.make_response(flask.jsonify(**context), 201)
            else:
                context = {
                    "logname": flask.session['user'],
                    "message": "Conflict",
                    "postid": postid_url_slug,
                    "status_code": 409
                }
                return flask.make_response(flask.jsonify(**context), 409)
    else:
        flask.abort(403)
        return None
