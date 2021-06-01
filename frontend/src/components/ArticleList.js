import React, { Component } from "react";
import { Link } from "react-router-dom";

var delayTimer;

class ArticleList extends Component {
  state = {
    isLoading: true,
    articles: [],
  };

  componentDidMount() {
    this._fetchArticles();
  }

  _fetchArticles = async () => {
    const response = await fetch(
      "http://localhost:5000/latest"
    ).then((response) => response.json());

    this.setState({
      articles: response,
      isLoading: false,
    });
    console.log(this.state.articles);
  };

  _onSearch = async (e) => {
    clearTimeout(delayTimer);
    delayTimer = setTimeout(async () => {
      const keyword = e.target.value;
      const response = await fetch(
        `http://localhost:5000/search/${keyword}`
      ).then((response) => response.json());

      this.setState({
        articles: response,
        isLoading: false,
      });
    }, 1000); // Will do the ajax stuff after 1000 ms, or 1 s
  };

  render() {
    const { isLoading, articles } = this.state;

    return (
      <div className="home-articles-list">
        <h4 className="headline">Seneste artikler</h4>
        <form>
          <input
            type="text"
            className="form-control"
            placeholder="Søg efter artikler"
            onChange={this._onSearch}
          />
        </form>
        <div className="list">
          {!isLoading && articles.length === 0 ? (
            <p>Fandt ingen artikler..s</p>
          ) : (
            articles.map((item) => {
              return <Article {...item} />;
            })
          )}
        </div>
      </div>
    );
  }
}

const Article = ({ headline, excerpt, article_id }) => {
  return (
    <div className="article">
      <Link to={`/article/${article_id}`}>
        <h2 className="title">{headline}</h2>
      </Link>
      <p className="excerpt">
        {excerpt}
      </p>
    </div>
  );
};

export default ArticleList;
