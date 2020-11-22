"""Views, one for each Insta485 page."""
from insta485.views.user import show_user

from insta485.views.index import serve_css
from insta485.views.index import serve_image

from insta485.views.index import show_index
from insta485.views.explore import show_explore
from insta485.views.post import show_post
from insta485.views.followers import show_followers
from insta485.views.following import show_following

from insta485.views.account_login_logout import show_acclogin
from insta485.views.account_login_logout import exec_logout
from insta485.views.account_create import show_acc_create
from insta485.views.account_delete import show_acc_delete
from insta485.views.account_edit import show_acc_edit
from insta485.views.account_password import show_acc_passwd
