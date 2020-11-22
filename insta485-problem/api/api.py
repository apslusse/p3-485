"""REST API"""
import flask
import insta485


@insta485.app.route('/api/v1/',  methods=["GET"])
def show_resources():
    """Return API resource URLs"""
    resources = {
    "posts": "/api/v1/p/",
    "url": "/api/v1/"
    }
    return flask.jsonify(resources)


@insta485.app.route('/api/v1/p/',  methods=["GET"])
def show_posts():
    """Return posts based on size and page variables"""
    if "user" in flask.session:
        curr_user = flask.session['user']
        cur = insta485.model.get_db().execute(
            "SELECT "
            "posts.postid "
            "FROM posts "
            "INNER JOIN following AS userfollow ON following.username1=? "
            "INNER JOIN following ON following.username2=posts.owner "
            "GROUP BY posts.postid "
            "ORDER BY posts.postid DESC", (curr_user,)
        )
        posts = cur.fetchall()

        # Fetch users own posts
        cur = insta485.model.get_db().execute(
            "SELECT postid "
            "FROM posts "
            "WHERE owner=?", (curr_user,)
        )
        profile_pic = cur.fetchall()

        # Append profile_pic (self_posts) to posts. Style workaround.
        posts = profile_pic + posts
        topTen = []

        size = flask.request.args.get("size", default=10, type=int)
        page = flask.request.args.get("page", default=0, type=int)

        if size < 1 or page < 0:
            postDictionary = {
                "message": "Bad Request",
                "status_code": 400
            }
            return flask.jsonify(postDictionary)

        # Sort new posts by postid.
        posts.sort(key=lambda x: x['postid'])
        numberPosts = 0
        next = ""
        numberSkip = page * size
        numberSeen = 0
        posts = list(reversed(posts))
        for post in posts:
            if numberSeen < numberSkip:
                numberSeen += 1
            elif numberPosts < size:
                post["url"] = "/api/v1/p/" + str(post["postid"]) + "/"
                topTen.append(post)
                numberPosts += 1
            else:
                next = "/api/v1/p/?size=" + str(size) + "&page=" + str(page + 1)
        postDictionary = {
            "next": next,
            "results": topTen,
            "url": "/api/v1/p/"
        }
        return flask.jsonify(postDictionary)
    else:
        flask.abort(403)
        return None


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/', methods=["GET"])
def get_post(postid_url_slug):
    """Get post for postid"""
    if "user" in flask.session:
        cur = insta485.model.get_db().execute(
            "SELECT "
            "posts.created, posts.filename, posts.owner "
            "FROM posts WHERE posts.postid=? ",
            (postid_url_slug,)
        )
        posts = cur.fetchall()
        cur1 = insta485.model.get_db().execute(
            "SELECT "
            "users.filename "
            "FROM users WHERE users.username=? ",
            (posts[0]['owner'],)
        )
        user = cur1.fetchall()

        post = {
            "age": posts[0]['created'],
            "img_url": "/uploads/" + posts[0]['filename'],
            "owner": posts[0]['owner'],
            "owner_img_url": "/uploads/" + user[0]['filename'],
            "owner_show_url" : "/u/" + posts[0]['owner'] + "/",
            "post_show_url" : "/p/" + str(postid_url_slug) + "/",
            "url": "/api/v1/p/" + str(postid_url_slug) + "/"
        }
        return flask.jsonify(post)
    else:
        flask.abort(403)
        return None


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/comments/',
 methods=["GET","POST"])
def get_post_comments(postid_url_slug):
    """Return comments for postid or post a comment"""
    if "user" in flask.session:
        if flask.request.method == 'GET':
            #return comments
            cur = insta485.model.get_db().execute(
                "SELECT * "
                "FROM comments WHERE postid=?", (postid_url_slug,)
            )
            comments = cur.fetchall()
            post_comments = {
                "comments": [],
                "url": "/api/v1/p/" + str(postid_url_slug) + "/comments/",
            }
            for comment in comments:
                dictcomment = {
                    "commentid": comment['commentid'],
                    "owner": comment['owner'],
                    "owner_show_url": "/u/" + comment['owner'] + "/",
                    "postid": comment['postid'],
                    "text": comment['text'],
                }
                post_comments["comments"].append(dictcomment)
            return flask.jsonify(**post_comments)
        else:
            #post a comment
            cur = insta485.model.get_db().execute(
                "SELECT MAX(commentid) FROM comments"
            )
            maxcomment = cur.fetchall()
            nextCommentId = 0
            if maxcomment[0]["MAX(commentid)"] != None:
                nextCommentId = int(maxcomment[0]["MAX(commentid)"]) + 1
            commentDict = {
                "commentid": nextCommentId,
                "owner" : flask.session["user"],
                "owner_show_url": "/u/" + flask.session["user"] + "/",
                "postid": postid_url_slug,
                "text" : flask.request.json.get("text")
            }

            cur2 = insta485.model.get_db().execute(
                "INSERT INTO comments (commentid, owner, postid, text) VALUES "
                "(?, ?, ?, ?)", (commentDict['commentid'],commentDict['owner'],
                commentDict['postid'],commentDict['text'])
            )

            return flask.make_response(flask.jsonify(commentDict), 201)

    else:
        flask.abort(403)
        return None
