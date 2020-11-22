import React from 'react';
import PropTypes from 'prop-types';

class CommentBar extends React.Component {
  // Comment Form Dubmission for a Post

  render(){
    const post_id = this.props.post_id
    const url = this.props.url

    return (
      <form action={ url } method="post" encType="multipart/form-data">
        <input type="hidden" name="postid" value={ post_id }/>
        <input type="text" name="text"/>
        <input type="submit" name="comment" value="comment"/>
      </form>

    );
  }


}
export default CommentBar;
