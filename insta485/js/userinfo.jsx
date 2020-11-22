import React from 'react';
import PropTypes from 'prop-types';

class UserInfo extends React.Component {
  // Display user profile picture, username in a post

  render(){
    const { poster_ppurl } = this.props;
    console.log(poster_ppurl);
    const { poster_url } = this.props;
    const { poster_name } = this.props;
    return (
      <div className="post-bar">
        <a href={poster_url}>
          <img src={poster_ppurl} alt="PosterProfilePicture" className="profile-pic"/>
        </a>
        <a href={poster_url} className="post-user">
          {poster_name}
        </a>
      </div>

    );
  }


}

export default UserInfo;
