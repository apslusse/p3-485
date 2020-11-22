import React from 'react';
import PropTypes from 'prop-types';
import UserInfo from './userinfo';
import Timestamp from './timestamp';
import Picture from './picture';
import Likes from './likes';
import Comments from './comments';


class Post extends React.Component {
  // Generate Posts
  constructor(props){
    super(props);
    this.state = {
      timestamp: "YYYY-MM-DD HH:MM:SS",
      poster_url: null,
      poster_ppurl: null,
      poster_username: null,
      post_img_url: null,
      post_url: null,
      api_url: this.props.post_api_url
    };
    this.child = React.createRef();
  }



  updateLike(){
    const { logname_likes_this } = this.state;
    const { numLikes } = this.state;
    let request = 'POST';

    if(logname_likes_this){
      this.setState({
        numLikes: numLikes - 1,
        logname_likes_this: !logname_likes_this
      });

      request = 'DELETE'
    }
    else{
      this.setState({
        numLikes: numLikes + 1,
        logname_likes_this: !logname_likes_this
      });

    }
    const { post_api_url } = this.props;

    const data = {}
    fetch(post_api_url + "likes/", {
      method: request,
      credentials: 'same-origin',
      body: JSON.stringify(data)
    })
    .then((response) =>{
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    })
    .then((data) => {

    })
    .catch((error) => console.log(error));

  }

  handleClick() {
    const { numLikes } = this.state;
    const { logname_likes_this } = this.state;
    const { post_api_url } = this.props;
    if (logname_likes_this == 1){
      return;
    }
    else{
      fetch(post_api_url + "likes/", {credentials: 'same-origin', method: 'post' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response;
        })
        .then((response) => {
          this.setState({
            numLikes: numLikes + 1,
            logname_likes_this: 1,
          });

          console.log("LIKE");
        })
        .catch((error) => console.log(error));
      }
    }

  componentDidMount() {
    const { post_api_url } = this.props;

    fetch(post_api_url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          timestamp: data.age,
          poster_ppurl: data.owner_img_url,
          poster_url: data.owner_show_url,
          poster_username: data.owner,
          post_img_url: data.img_url,
          post_url: data.post_show_url,
          api_url: data.url,
          focus: 0,
        });
      })
      .catch((error) => console.log(error));

      fetch(post_api_url + "likes/", { credentials: 'same-origin' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);

          return response.json();
        })
        .then((data) => {
          this.setState({
            numLikes: data.likes_count,
            logname_likes_this: data.logname_likes_this,
          });

        })
        .catch((error) => console.log(error));

  }

  render(){
    const { post_id } = this.props;
    const { poster_ppurl } = this.state;
    const { poster_url } = this.state;
    const { poster_username } = this.state;
    const { timestamp } = this.state;
    const { post_url } = this.state;
    const { post_img_url } = this.state;
    const { api_url } = this.state;
    const { logname_likes_this } = this.state;
    const { numLikes } = this.state;
    const { focus } = this.state;


    return (
      <div className="post">
        <UserInfo poster_ppurl = {poster_ppurl} poster_url = {poster_url} poster_name = {poster_username}  />
        <Timestamp post_url = {post_url} timestamp = {timestamp}/>
        <Picture picture_url = {post_img_url} onClick={() => this.handleClick()} />
        <Likes url = {`${this.props.post_api_url}likes/`} onClick={() => this.updateLike()} numLikes = { numLikes } logname_likes_this = { logname_likes_this } />
        <Comments api_url = {api_url} post_url = {post_url} post_id = {post_id}/>
      </div>
    );
  }


}

/*
Post.propTypes = {
  url: PropTypes.string.isRequired,
};
*/
export default Post;
