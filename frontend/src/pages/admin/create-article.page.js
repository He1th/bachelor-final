import { Component } from "react";
import AdminLayout from "../../components/AdminLayout";

class CreateArticle extends Component {
  onSubmit = async (e) => {
    e.preventDefault();
    var formData = new FormData(e.target);

    const response = await fetch("http://localhost:5000/admin/create-article", {
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

  render() {
    return (
      <AdminLayout active={2}>
        <div className="row">
          <div className="col-md-8">
            <div>
              <h4>Admin panel</h4>
              <p>Tilpas algoritmen.</p>
            </div>
            <form action="#" method="POST" onSubmit={this.onSubmit}>
              <div className="form-group mb-3">
                <label>Overskrift</label>
                <input type="text" name="headline" className="form-control" />
              </div>
              <div className="form-group mb-3">
                <label>Indledning</label>
                <input type="text" name="excerpt" className="form-control" />
              </div>
              <div className="form-group mb-3">
                <label>Forfatter</label>
                <input type="text" name="author" className="form-control" />
              </div>
              <div className="form-group mb-3">
                <label>Indhold</label>
                <textarea type="text" name="text" className="form-control" />
              </div>
              <button className="btn btn-primary" type="submit">
                Opret artikel
              </button>
            </form>
          </div>
        </div>
      </AdminLayout>
    );
  }
}

export default CreateArticle;
