import { Component } from "react";
import { BrowserRouter as Route, Switch } from "react-router-dom";
import AdminLayout from "../../components/AdminLayout";
import User from "../../utils/user";

class AdminPage extends Component {
  state = {
    users: [],
  };

  componentDidMount() {
    this._fetchData();
  }

  _onClick = (username) => {
    User.setUser(username);
  };

  _onCreateUser = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    console.log(e.target);
    const response = await fetch(
      `http://localhost:5000/admin/createUser/${formData.get("username")}`
    ).then((response) => response.json());
    this._fetchData();
  };

  _onResetUser = async (username) => {
    fetch(`http://localhost:5000/admin/resetUser/${username}`).then(
      (response) => response.json()
    );
    alert("Denne brugers artikler er nu resat");
  };

  _fetchData = async () => {
    const response = await fetch(`http://localhost:5000/admin/getUsers`).then(
      (response) => response.json()
    );
    console.log(response.data);
    this.setState({
      isLoading: false,
      users: response.data,
    });
  };

  render() {
    const { users } = this.state;
    return (
      <AdminLayout active={3}>
        <div>
          <h4>Bruger liste</h4>
          <p>Vælg en bruger fra listen eller opret en ny.</p>
          <div>
            <form action="#" method="#" onSubmit={this._onCreateUser}>
              <input
                type="text"
                name="username"
                className="form-control"
                placeholder="indtast brugernavn"
              />
              <button className="btn btn-primary mt-3">Tilføj bruger</button>
            </form>
          </div>
          <hr />
          <div className="list">
            <ul>
              {users &&
                users.map((user) => (
                  <li>
                    <div className="d-flex">
                      <div className="full-width">{user}</div>
                      <div className="ml-auto" style={{ width: "240px" }}>
                        <button
                          className="btn btn-sm btn-primary"
                          onClick={() => this._onClick(user)}
                        >
                          Aktiver
                        </button>
                        <button
                          style={{ marginLeft: "10px" }}
                          className="btn btn-sm btn-dark"
                          onClick={() => this._onResetUser(user)}
                        >
                          Reset bruger
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
            </ul>
          </div>
        </div>
      </AdminLayout>
    );
  }
}

export default AdminPage;
