class User {
  setUser(username) {
    localStorage.setItem("user", username);
  }

  getUser() {
    const user = localStorage.getItem("user");
    return user ? user : 1;
  }
}

export default new User();
