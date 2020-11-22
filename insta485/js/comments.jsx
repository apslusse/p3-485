import React from 'react';
import PropTypes from 'prop-types';
import CommentRow from './commentrow';


class Comments extends React.Component {
  // Display commentTable for a Post
  constructor(props){
    super(props);
    this.state={
      comments: [],
      url:null,
      value:''
    }
    this.handleChange = this.handleChange.bind(this);


  }

  componentDidMount() {
    //console.log("comments--top");
    //console.log(this.props.api_url);
    //console.log("comments--bottom");
    const {api_url} = this.props;
    //console.log(api_url);
    const comments_url = `${api_url}comments/`;
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

  handleChange(event) {

    if(event.charCode==13){
      event.preventDefault();
      const data_new = {text: event.target.value};
      event.target.value = '';
      //url generation for fetch(POST~/comments)
      const {api_url} = this.props;
      const comments_url = api_url + "comments/";

      console.log(data_new);

      fetch( comments_url, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{'content-type': 'application/json'},
        body: JSON.stringify(data_new)
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        //generating the current state.comments

        console.log(this.state.comments);
        const commentDict = {
                  "commentid": data.commentid,
                  "owner" : data.owner,
                  "owner_show_url": "/u/" + data.owner + "/",
                  "postid": data.postid,
                  "text" : data.text
              }

        this.setState({
          comments: this.state.comments.concat(commentDict),
          url: this.state.url,
          value: ''
        });

      })
      .catch((error) => console.log(error));

    }
    else{
      const {comments} = this.state;
      const {url} = this.state;
      this.setState({
        comments:comments,
        url: url,
        value: event.value
      });
    }

  }

  //what happens when we submit a new comment. WE POST




  render(){
    const { comments } = this.state;
    //const { post_url } = this.state; this is the same as this.props.post_url


    const {post_url} = this.props;
    const {post_id} = this.state;


    return (

      <div className="comments">
      {comments.map((comment) =>
        <CommentRow
          key = {comment.commentid.toString()}
          comment_id = {comment.commentid}
          commenter_username = {comment.owner}
          commenter_url = {comment.owner_show_url}
          post_id = {comment.postid}
          text = {comment.text}
        />)}
        <form className="comment-form">
          <input type="text" onKeyPress={this.handleChange} onChange={this.handleChange} />
        </form>
      </div>
    );
  }


}

export default Comments;
