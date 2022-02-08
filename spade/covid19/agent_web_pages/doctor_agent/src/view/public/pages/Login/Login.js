import React, {Component} from 'react';
import {
  Button,
  Card,
  CardBody,
  CardGroup,
  Col,
  Container,
  Form,
  Input,
  InputGroup,
  InputGroupAddon,
  InputGroupText,
  Popover,
  PopoverBody,
  PopoverHeader,
  Row
} from 'reactstrap';
import {PublicHeader} from "../../components";
import {logIn} from "../../../../controller/ServerApi";
import {log} from '../../../../utils/Logging'
import './Login.css'

const currentScriptName = "Login.js";

class Login extends Component {

  constructor(props) {
    super(props);

    this.state = {
      username: '',
      password: '',
      fetchingUserData: false,
      forgotPasswordPopoverOpen: false,
    };

    this.toggleForgotPasswordPopover = this.toggleForgotPasswordPopover.bind(this);
  }

  toggleForgotPasswordPopover() {
    this.setState({
      forgotPasswordPopoverOpen: !this.state.forgotPasswordPopoverOpen,
    });
  }

  handleUsernameChanged(e) {
    this.setState({username: e.target.value});
  }

  handlePasswordChanged(e) {
    this.setState({password: e.target.value});
  }

  async handleLoginRequest(_) {
    this.setState({fetchingUserData: true});
    let authenticatedUser = await logIn(this.state.username, this.state.password);
    this.setState({fetchingUserData: false});

    this.props.saveLoggedUser(authenticatedUser);
    log(currentScriptName, "User logged in: ", authenticatedUser);
    this.props.refreshLoggedStatus()
  }

  render() {
    return (
      <div className="app flex-row align-items-center">
        <Container>
          <div className="fixed-top">
            <PublicHeader showNav={false}/>
          </div>
          <div className="animated fadeIn">
            <Row className="justify-content-center">
              {/* WITH REGISTER TAB THIS VALUE WAS md=8*/}
              <Col md="4">
                <CardGroup>
                  <Card className="p-4">
                    <CardBody>
                      <Form onKeyPress={
                        event => {
                          if (event.key === 'Enter') return this.handleLoginRequest(event)
                        }
                      }>
                        <h1>Login</h1>
                        <p className="text-muted">Sign In to your account</p>
                        <InputGroup className="mb-3">
                          <InputGroupAddon addonType="prepend">
                            <InputGroupText>
                              <i className="icon-user"/>
                            </InputGroupText>
                          </InputGroupAddon>
                          <Input type="text" placeholder="Username" autoComplete="username"
                                 onChange={this.handleUsernameChanged.bind(this)}/>
                        </InputGroup>
                        <InputGroup className="mb-4">
                          <InputGroupAddon addonType="prepend">
                            <InputGroupText>
                              <i className="icon-lock"/>
                            </InputGroupText>
                          </InputGroupAddon>
                          <Input type="password" placeholder="Password" autoComplete="current-password"
                                 onChange={this.handlePasswordChanged.bind(this)}/>
                        </InputGroup>
                        <Row>
                          <Col xs="6">
                            {
                              this.state.fetchingUserData
                                ? <Button color="grey" className="px-4" disabled={true}
                                          onClick={this.handleLoginRequest.bind(this)}>
                                  <img className='spinner' alt="spinner"
                                       src={require('../../../../assets/img/spinner.gif')}/>
                                </Button>
                                : <Button color="primary" className="px-4"
                                          onClick={this.handleLoginRequest.bind(this)}>Login</Button>
                            }
                          </Col>
                          <Col xs="6" className="text-right">
                            <Button color="link" className="px-0" id="ForgotPassword">Forgot password?</Button>
                            <Popover placement="bottom" target="ForgotPassword"
                                     isOpen={this.state.forgotPasswordPopoverOpen}
                                     toggle={this.toggleForgotPasswordPopover}>
                              <PopoverHeader>Help Tip!</PopoverHeader>
                              <PopoverBody>Try to click Login anyway <i
                                className="fa fa-smile-o fa-lg mt-4"/></PopoverBody>
                            </Popover>
                          </Col>
                        </Row>
                      </Form>
                    </CardBody>
                  </Card>
                  {/* DISABLED REDIRECTION TO REGISTER LINK*/}
                  {/*<Card className="text-white bg-primary py-5 d-md-down-none" style={{width: '44%'}}>*/}
                  {/*  <CardBody className="text-center">*/}
                  {/*    <div>*/}
                  {/*      <h2>Sign up</h2>*/}
                  {/*      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut*/}
                  {/*        labore et dolore magna aliqua.</p>*/}
                  {/*      <Link to="/register">*/}
                  {/*        <Button color="primary" className="mt-3" active tabIndex={-1}>Register Now!</Button>*/}
                  {/*      </Link>*/}
                  {/*    </div>*/}
                  {/*  </CardBody>*/}
                  {/*</Card>*/}
                </CardGroup>
              </Col>
            </Row>
          </div>
        </Container>
      </div>
    );
  }
}

export default Login;
