import React from 'react';
import PropTypes from 'prop-types';

class CommentRow extends React.Component {
  // Display a comment in CommentTable

  render(){
  const { comment_id } = this.props;
  const { commenter_username } = this.props;
  const { commenter_url } = this.props;
  const { post_id } = this.props;
  const { text } = this.props;

    return (
      <div className="post-comment">
        <a href={commenter_url} className="comment-user">{commenter_username}</a>
        <div className='comment-content'>
          <p>{text}</p>
        </div>
      </div>
    );
  }


}

export default CommentRow;
