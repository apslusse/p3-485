import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';

class Timestamp extends React.Component {
  // Display timestamp in a post

  render(){

    const { timestamp } = this.props; // <--CHANGE TO HRT later YYYY-MM-DD HH:MM:SS
    const { post_url } = this.props;
    const hrt = moment(timestamp).fromNow();

    return (
      <a href={post_url} className="post-time">
        {hrt}
      </a>
    );
  }


}

export default Timestamp;
