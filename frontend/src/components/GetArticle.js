import React, { Component } from "react";
import { withRouter } from "react-router";
import User from "../utils/user";
import { Link } from "react-router-dom";

class GetArticle extends Component {
  state = {
    isLoading: true,
    article: {},
  };

  componentDidMount() {
    this._fetchArticles();
  }

  componentDidUpdate(prevProps) {
    const prevID = prevProps.match.params.id;
    const newID = this.props.match.params.id;
    if (prevID !== newID) {
      this._fetchArticles();
    }
  }

  _fetchArticles = async () => {
    const username = User.getUser();
    const { id } = this.props.match.params;
    const response = await fetch(
      `http://localhost:5000/article/${id}/${username}`
    ).then((response) => response.json());

    this.setState({
      article: response,
      isLoading: false,
    });
    console.log(this.state.articles);
  };

  render() {
    const { isLoading, article } = this.state;
    if (isLoading) return null;

    const { headline, text } = article;

    return (
      <div className="home-articles-list">
        <h4 className="headline">{headline}</h4>
        <p>{text}</p>
      </div>
    );
  }
}

export default withRouter(GetArticle);
