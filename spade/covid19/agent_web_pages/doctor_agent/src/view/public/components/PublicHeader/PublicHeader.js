import React from 'react';
import {Button, ButtonGroup, Container, Nav, Navbar, NavbarBrand} from 'reactstrap';
import './PublicHeader.css'
import {Link} from "react-router-dom";


class PublicHeader extends React.Component {

  render() {
    const navButtons = (
      <Nav className="ml-auto" navbar>
        <ButtonGroup>
          <Link to="/login">
            <Button color="primary">
              <span className="d-sm-none d-xs-none"><i className="nc-icon nc-lock-circle-open access"/></span>
              <span className="d-none d-sm-block d-md-block d-lg-block d-xl-block">Login</span>
            </Button>
          </Link>
          {/*DISABLED REGISTRATION LINK IN HEADER*/}
          {/*<Link to="/register">*/}
          {/*  <Button color="warning">*/}
          {/*    <span className="d-sm-none d-xs-none"><i className="nc-icon nc-badge access"/></span>*/}
          {/*    <span className="d-none d-sm-block d-md-block d-lg-block d-xl-block">Register</span>*/}
          {/*  </Button>*/}
          {/*</Link>*/}
        </ButtonGroup>
      </Nav>
    );

    return (
      <Navbar color="dark" expand="true" className="navbar-absolute">
        <Container fluid>
          <div>
            <img className="logo-img" src={require("../../../../assets/img/brand/sygnet.svg")} alt="Logo"/>
            <NavbarBrand>Covid19 Project</NavbarBrand>
          </div>
          {this.props.showNav ? navButtons : null}
        </Container>
      </Navbar>
    );
  }
}

export default PublicHeader;
