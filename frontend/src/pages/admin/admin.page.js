import { Component } from "react";
import { BrowserRouter as Route, Switch } from "react-router-dom";
import AdminLayout from "../../components/AdminLayout";
import CreateArticle from "./create-article.page";

class AdminPage extends Component {
  state = {
    data: [],
  };

  componentDidMount() {
    this._fetchData();
  }

  _handleChange = (id, value) => {
    var data = this.state.data;
    this.setState({ data: { ...this.state.data, [id]: value } });
  };

  _onSubmit = async (e) => {
    e.preventDefault();
    var formData = new FormData(e.target);

    const response = await fetch("http://localhost:5000/admin/setParameters", {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      //credentials: "same-origin", // include, *same-origin, omit
      headers: {
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      body: formData, // body data type must match "Content-Type" header
    });
    console.log(response);
  };

  _fetchData = async () => {
    const response = await fetch(`http://localhost:5000/admin/parameters`).then(
      (response) => response.json()
    );
    this.setState({
      data: response,
    });
    console.log(response);
  };

  render() {
    const { data } = this.state;
    return (
      <AdminLayout active={1}>
        <div>
          <h4>Admin panel</h4>
          <p>Tilpas algoritmen.</p>
          <div className="row">
            <div className="col-md-6">
              <form action="#" method="POST" onSubmit={this._onSubmit}>
                <div className="form-group mb-3">
                  <label>Headline vægt</label>
                  <input
                    type="number"
                    name="headline"
                    className="form-control"
                    onChange={(e) => this._handleChange(1, e.target.value)}
                    value={data[1]}
                    min="0"
                    step=".01"
                    max="5"
                  />
                </div>
                <div className="form-group mb-3">
                  <label>Excerpt vægt</label>
                  <input
                    type="number"
                    name="excerpt"
                    className="form-control"
                    onChange={(e) => this._handleChange(2, e.target.value)}
                    value={data[2]}
                    min="0"
                    step=".01"
                    max="5"
                  />
                </div>
                <div className="form-group mb-3">
                  <label>Text vægt</label>
                  <input
                    type="number"
                    name="text"
                    value={data[3]}
                    className="form-control"
                    onChange={(e) => this._handleChange(3, e.target.value)}
                    min="0"
                    step=".01"
                    max="5"
                  />
                </div>
                <div className="form-group mb-3">
                  <label>Noun vægt</label>
                  <input
                    type="number"
                    name="noun"
                    value={data[4]}
                    className="form-control"
                    onChange={(e) => this._handleChange(4, e.target.value)}
                    min="0"
                    step=".01"
                    max="5"
                  />
                </div>
                <div className="form-group mb-3">
                  <label>Name vægt</label>
                  <input
                    type="number"
                    name="name"
                    onChange={(e) => this._handleChange(5, e.target.value)}
                    value={data[5]}
                    className="form-control"
                    min="0"
                    step=".01"
                    max="5"
                  />
                </div>
                <div className="form-group mb-3">
                  <label>Location vægt</label>
                  <input
                    type="number"
                    name="location"
                    onChange={(e) => this._handleChange(6, e.target.value)}
                    value={data[6]}
                    className="form-control"
                    min="0"
                    step=".01"
                    max="5"
                  />
                </div>
                <div className="form-group mb-3">
                  <label>Organisation vægt</label>
                  <input
                    type="number"
                    onChange={(e) => this._handleChange(7, e.target.value)}
                    value={data[7]}
                    name="organisation"
                    className="form-control"
                    min="0"
                    step=".01"
                    max="5"
                  />
                </div>
                <div className="form-group mb-3">
                  <label>Antal seneste artikler</label>
                  <input
                    type="number"
                    name="articles"
                    onChange={(e) => this._handleChange(8, e.target.value)}
                    className="form-control"
                    value={data[8]}
                    min="0"
                    step=".01"
                    max="5000"
                  />
                </div>
                <div className="form-group mb-3">
                  <label>Antal anbefaldede artikler</label>
                  <input
                    type="number"
                    name="recommendedArticles"
                    className="form-control"
                    onChange={(e) => this._handleChange(9, e.target.value)}
                    value={data[9]}
                    min="0"
                    step=".01"
                    max="5000"
                  />
                </div>
                <button className="btn btn-primary" type="submit">
                  Gem
                </button>
              </form>
            </div>
          </div>
        </div>
      </AdminLayout>
    );
  }
}

export default AdminPage;
