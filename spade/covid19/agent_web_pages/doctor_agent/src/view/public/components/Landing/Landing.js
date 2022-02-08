import React from 'react';
import {Col, Container, Row} from 'reactstrap';
import './Landing.scss'

const Landing = () => {
  return (
    <Container>
      <Row>
        <Col>
          <div className="logo-center">
            <img src={require("../../../../assets/img/brand/sygnet.svg")} alt="Covid19 Logo"/>
          </div>
        </Col>
      </Row>
      <div className="animated fadeIn">
        <Row>
          <Col className="land pr-0">
            <header>
              <div className="container--lg border--bottom pb3 ">
                <h1 className="mb2">Physical activity at Covid19 time</h1>
                <div className="shadow-separator"/>
              </div>
            </header>
          </Col>
        </Row>
        <Row>
          <div className="info grid-wrapper">
            <div>
              <h2>Data Usage</h2>
              <p>
                Quis istud possit, inquit, negare? Videamus animi partes, quarum est conspectus illustrior;
                Illa sunt similia: hebes acies est cuipiam oculorum, corpore alius senescit; Non enim, si omnia non
                sequebatur.
                Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur
                magni
                dolores eos,
                qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit,
                amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore
                magnam aliquam quaerat voluptatem.
              </p>
              <hr/>
              <p className="sub">
                Ea cupidatat quis est pariatur est proident id et non officia sit velit.
                Ad consectetur esse do consequat.
              </p>
              <p className="cit">Enrico Siboni - IT Assistant @ HES-SO</p>
            </div>
            <div className="info-img">
              <img src={require("../../../../assets/img/data.svg")} alt="Data"/>
            </div>
          </div>
          <div className="info grid-wrapper">
            <div className="info-img">
              <img src={require("../../../../assets/img/security.svg")} alt="Security"/>
            </div>
            <div>
              <h2>Absolute security</h2>
              <p>
                Quis istud possit, inquit, negare? Videamus animi partes, quarum est conspectus illustrior;
                Illa sunt similia: hebes acies est cuipiam oculorum, corpore alius senescit; Non enim, si omnia non
                sequebatur.
                Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi architecto beatae vitae dicta
                sunt, explicabo.
              </p>
              <hr/>
              <p className="sub">
                Ea id reprehenderit cupidatat incididunt labore ullamco quis qui velit ex nostrud exercitation veniam.
              </p>
              <p className="cit">Davide Calvaresi - PostDoctoral Researcher @ HES-SO</p>
            </div>
          </div>
          <div className="info grid-wrapper">
            <div>
              <h2>Research</h2>
              <p>
                Quis istud possit, inquit, negare? Videamus animi partes, quarum est conspectus illustrior;
                Illa sunt similia: hebes acies est cuipiam oculorum, corpore alius senescit; Non enim, si omnia non
                sequebatur.
                Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur
                magni
                dolores eos,
                qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit,
                amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore
                magnam aliquam quaerat voluptatem.
              </p>
              <hr/>
              <p className="sub">
                Labore ipsum deserunt ullamco magna.
                Sit velit dolor in do in in anim sint.
              </p>
              <p className="cit">Michael I. Schumacher - Professor @ HES-SO</p>
            </div>
            <div className="info-img">
              <img src={require("../../../../assets/img/assign.svg")} alt="Research"/>
            </div>
          </div>
        </Row>
      </div>
      <div className="shadow-separator"/>
    </Container>
  );
};

export default Landing;
