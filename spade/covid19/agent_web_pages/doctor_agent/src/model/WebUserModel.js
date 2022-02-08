class WebUserModel {

  constructor({name = "", surname = "", email = "", role = ""}) {
    this.name = name;
    this.surname = surname;
    this.email = email;
    this.role = role;
  }

}

export {WebUserModel}
