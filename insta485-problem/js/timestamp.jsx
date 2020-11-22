import React from 'react';
import PropTypes from 'prop-types';

class Timestamp extends React.Component {
  // Display timestamp in a post

  render(){
    console.log(`${timestamp}: is the time`);
    const { timestamp } = this.props // <--CHANGE TO HRT later
    const { post_url } = this.props
    return (
      <a href={post_url} className="post-time">
        {timestamp}
      </a>
    );
  }


}

export default Timestamp;
