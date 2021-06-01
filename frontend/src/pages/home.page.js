import { Component } from "react";
import ArticleList from "../components/ArticleList";
import RecommendedArticleList from "../components/RecommendedArticleList";

class Home extends Component {
  render() {
    return (
      <div className="row">
        <div className="col-md-7">
          <ArticleList />
        </div>
        <div className="col-md-4 offset-1">
          <RecommendedArticleList />
        </div>
      </div>
    );
  }
}

export default Home;
