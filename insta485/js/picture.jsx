import React from 'react';
import PropTypes from 'prop-types';

class Picture extends React.Component {
  //Display Picture of a post

  render(){
    const { picture_url } = this.props;

    return(
      <img src={picture_url} alt="PostPicture" className='post-photo'
      onDoubleClick={() => this.props.onClick()} />
    );
  }


}
export default Picture;
