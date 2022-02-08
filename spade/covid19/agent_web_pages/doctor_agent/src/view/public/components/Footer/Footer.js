import React from "react";
import {Container, Row} from "reactstrap";
import './Footer.css'
// used for making the prop types of this component
import PropTypes from "prop-types";

class Footer extends React.Component {
  render() {
    return (
      <footer className={"footer" + (this.props.default ? " footer-default" : "")}>
        <Container fluid={this.props.fluid}>
          <Row>
            <nav className="footer-nav">
              {/*<a href="https://scodes.ch/" target="_blank" rel="noopener noreferrer">*/}
              Covid19 Project
              {/*</a>*/}
            </nav>
            <div className="credits ml-auto">
              <div className="copyright">
                &copy; {1900 + new Date().getYear()}, made with <i className="fa fa-heart heart"/> by Enrico Siboni
              </div>
            </div>
          </Row>
        </Container>
      </footer>
    );
  }
}

Footer.propTypes = {
  default: PropTypes.bool,
  fluid: PropTypes.bool
};

export default Footer;
