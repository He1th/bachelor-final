import { Component } from "react";
import { Link } from "react-router-dom";

class AdminLayout extends Component {
  render() {
    const { children, active } = this.props;
    return (
      <div className="row">
        <div className="col-md-3">
          <div
            class="nav flex-column nav-pills"
            id="v-pills-tab"
            role="tablist"
            aria-orientation="vertical"
          >
            <Link
              className={`nav-link ${active === 1 ? "active" : ""} `}
              to={"/admin/"}
            >
              Forside
            </Link>

            <Link
              className={`nav-link ${active === 2 ? "active" : ""} `}
              to={"/admin/create-article"}
            >
              Tilføj artikel
            </Link>

            <Link
              className={`nav-link ${active === 3 ? "active" : ""} `}
              to={"/admin/user-list"}
            >
              Bruger liste
            </Link>
          </div>
        </div>
        <div className="col-md-9">{children}</div>
      </div>
    );
  }
}

export default AdminLayout;
