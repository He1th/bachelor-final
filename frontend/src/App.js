import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Home from "./pages/home.page";
import Article from "./pages/article.page";
import AdminPage from "./pages/admin/admin.page";
import "./styles/style.css";
import CreateArticle from "./pages/admin/create-article.page";
import UsersList from "./pages/admin/users.page";

function App() {
  return (
    <Router>
      <div className="home">
        <div className="container">
          <Switch>
            <Route exact path="/admin/" component={AdminPage} />
            <Route
              exact
              path="/admin/create-article"
              component={CreateArticle}
            />
            <Route exact path="/admin/user-list" component={UsersList} />
            <Route exact path="/" component={Home} />
            <Route exact path="/article/:id" component={Article} />
          </Switch>
        </div>
      </div>
    </Router>
  );
}

export default App;
