import React from 'react';
import PropTypes from 'prop-types';

class LikeButton extends React.Component {
  // Display Likebutton for a Post

  render(){
  const { post_id } = this.props
  const { post_url } = this.props
  const { logname_likes_this } = this.props
    return (
      <div>
        <form action={ post_url } method="post" encType="multipart/form-data">
          <input type="hidden" name="postid" value={ post_id }/>
          <input type="submit" name="like" value={logname_likes_this ? 'unlike' : 'like'}/>
        </form>
      </div>
    );
  }


}
export default LikeButton;
