import React, { Component } from "react";
import { Link } from "react-router-dom";
import User from "../utils/user";

class RecommendedArticleList extends Component {
  state = {
    articles: [],
    isLoading: true,
  };

  async componentDidMount() {
    await setTimeout(() => {
      this._fetchArticles();
    }, 300);
  }

  _fetchArticles = async () => {
    const username = User.getUser();
    const response = await fetch(
      `http://localhost:5000/recommended/${username}`
    ).then((response) => response.json());

    this.setState({
      articles: response,
      isLoading: false,
    });
    console.log(this.state.articles);
  };

  render() {
    const { articles } = this.state;
    return (
      <div className="recommended-articles-list">
        {articles.length === 0 ? (
          <p>Fandt ingen artikler..</p>
        ) : (
          articles.map((item) => {
            return <Article {...item} />;
          })
        )}
      </div>
    );
  }
}

const Article = ({ headline, article_id }) => {
  return (
    <div className="article">
      <h2 className="title">
        <Link to={`/article/${article_id}`}>{headline}</Link>
      </h2>
    </div>
  );
};

export default RecommendedArticleList;
