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
    if(PerformanceNavigationTiming.type == "back_forward"){
      this.setState({
        posts: history.state.posts,
        next_url: history.state.next_url,
        url: history.state.url
      })
    return;
  }


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
      //pushing state to history stack
      history.pushState(this.state, null);

  }

  fetchMoreData(){
    const { next_url } = this.state;
    const {posts} = this.state;
    fetch(next_url, { credentials: 'same-origin' })
      .then((response) => {
        if(!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          posts: this.state.posts.concat(data.results),
          next_url: data.next, // <----- this is for next page
          url: data.url
        });
        console.log(this.state.posts)
      })
      .catch((error) => console.log(error));
      history.pushState(this.state, null);
  }


  render(){
    const {posts} = this.state;
    const {next_url} = this.state;
    var isNext = false;
    if (next_url){
      isNext = true;
    }
    return (
      <div className = "poststack">
      <InfiniteScroll
        dataLength={posts.length}
        next={() => this.fetchMoreData()}
        hasMore={isNext}
        loader={<h4>Loading...</h4>}
      >
        {posts.map((post) =>
          <Post key={post.postid.toString()} post_id={post.postid} post_api_url = {post.url}/>)}
      </InfiniteScroll>
      </div>
    );
  }


}


Poststack.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Poststack;
