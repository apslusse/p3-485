import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes and like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    const { focus } = this.props;
    console.log("constructor")



  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    // const likes_api_url = `${url}likes/`
    // Call REST API to get number of likes

  }



  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes
    const { numLikes } = this.props;
    const { logname_likes_this } = this.props;

    // Render number of likes

    return (
      <div>
      <button
        className="like-unlike-button"
        onClick ={() => this.props.onClick()}
        >
        <p>{logname_likes_this ? 'unlike' : 'like'}</p>
      </button>

      <div className = 'likes'>
        <p>
          {numLikes}
          {' '}
          like
          {numLikes !== 1 ? 's' : ''}
        </p>
      </div>
      </div>
    );
  }
}


/*
Likes.propTypes = {
  url: PropTypes.string.isRequired,
};
*/
export default Likes;
