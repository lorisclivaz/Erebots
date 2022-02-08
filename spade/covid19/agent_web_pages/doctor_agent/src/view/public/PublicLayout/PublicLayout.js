import React from "react";
import {Footer, Landing, PublicHeader} from '../components';
import {Container} from 'reactstrap';
import './PublicLayout.css';

class PublicLayout extends React.Component {

  render() {
    return (
      <Container>
        <div className="fixed-top">
          <PublicHeader showNav={true}/>
        </div>
        <div>
          <Landing/>
        </div>
        <Footer/>
      </Container>
    );
  }
}

export default PublicLayout;
