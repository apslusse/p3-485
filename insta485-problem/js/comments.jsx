import React from 'react';
import PropTypes from 'prop-types';
import CommentRow from './commentrow';
import CommentBar from './commentbar';

class Comments extends React.Component {
  // Display commentTable for a Post
  constructor(props){
    super(props);
    this.state={
      comments: [],
      url:null
    }
  }

  componentDidMount() {
    //console.log("comments--top");
    //console.log(this.props.api_url);
    //console.log("comments--bottom");
    const {api_url} = this.props;
    //console.log(api_url);
    const comments_url = `${api_url}comments/`
    //console.log(comments_url);

    fetch(comments_url, {credentials: 'same-origin'})
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          comments: data.comments,
          url: data.url
        });
      })
      .catch((error) => console.log(error));
  }
  render(){
    const { comments } = this.state;
    //const { post_url } = this.state; this is the same as this.props.post_url
    const listComments = comments.map((comment) =>
      <CommentRow
        key = {comment.commentid.toString()}
        comment_id = {comment.commentid}
        commenter_username = {comment.owner}
        commenter_url = {comment.owner_show_url}
        post_id = {comment.postid}
        text = {comment.text}
      />
    );

    const {post_url} = this.props;
    const {post_id} = this.state;


    return (

      <div className="comments">
        {listComments}
        <CommentBar post_url={post_url} post_id={post_id}/>
      </div>
    );
  }


}

export default Comments;
