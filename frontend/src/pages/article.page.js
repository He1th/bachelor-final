import { Component } from "react";
import GetArticle from "../components/GetArticle";
import RecommendedArticleList from "../components/RecommendedArticleList";

class ArticlePage extends Component {
  render() {
    return (
      <div className="row">
        <div className="col-md-7">
          <GetArticle />
        </div>
        <div className="col-md-4 offset-1">
          <RecommendedArticleList />
        </div>
      </div>
    );
  }
}

export default ArticlePage;
