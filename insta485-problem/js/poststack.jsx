import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';
import InfiniteScroll from 'react-infinite-scroll-component';

class Poststack extends React.Component {
  // Display posts in homepage

  constructor(props){
    super (props);
    this.state = {
      posts: [],
      next_url: null,
      url: null
    };
  }

  componentDidMount() {
    const { url } = this.props;

    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if(!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          posts: data.results,
          next_url: data.next, // <----- this is for next page
          url: data.url
        });
      })
      .catch((error) => console.log(error));
  }


  render(){
    const {posts} = this.state;
    const listPosts = posts.map((post) =>
      <Post key={post.postid.toString()} post_id={post.postid} post_api_url = {post.url}/>
    );

    return (
      <div className = "poststack">

        {listPosts}
      
      </div>
    );
  }


}


Poststack.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Poststack;
