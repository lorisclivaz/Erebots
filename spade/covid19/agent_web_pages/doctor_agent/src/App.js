import React, {Component} from 'react';
import {HashRouter, Redirect, Route, Switch} from 'react-router-dom';

import {instanceOf} from 'prop-types';
import {Cookies, withCookies} from 'react-cookie';
import './App.scss';
import {CookiesController} from "./controller/CookiesController";
import {AuthenticatedRoute, UnauthenticatedRoute} from './view/public/components/AuthenticationAwareRoutes'
import {AppState} from "./model/AppState";
import {createLoading} from "./utils/DataLoadingUtils";

// Containers
const Public = React.lazy(() => import('./view/public/PublicLayout'));
const DefaultLayout = React.lazy(() => import('./view/protected/DefaultLayout'));

// Pages
const Login = React.lazy(() => import('./view/public/pages/Login'));
const Register = React.lazy(() => import('./view/public/pages/Register'));
const Page404 = React.lazy(() => import('./view/public/pages/Page404'));
const Page500 = React.lazy(() => import('./view/public/pages/Page500'));

class App extends Component {

  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };

  constructor(props) {
    super(props);

    const {cookies} = props;
    this.cookiesController = new CookiesController(cookies);
    // this.cookiesController.eraseCookies(); // enable if wanted to start fresh every page reload
    this.cookiesController.loadStateOrDefault(this);
  }

  saveLoggedUser(user) {
    let appState = new AppState({user: user});
    this.cookiesController.saveStateToCookies(appState);
  }

  deleteLoggedUser() {
    this.cookiesController.eraseCookies();
  }

  refreshLoggedStatus() {
    this.cookiesController.loadStateOrDefault(this);
    this.setState({isAuthenticated: this.state.user !== undefined})
  }

  componentDidMount() {
    this.refreshLoggedStatus()
  }

  render() {
    // log("App props : ", this.props);
    return (
      <HashRouter>
        <React.Suspense fallback={createLoading({pt: 3, position: 'center'})}>
          <Switch>
            <UnauthenticatedRoute
              exact path="/login" name="Login Page" component={Login} appProps={this.state}
              refreshLoggedStatus={this.refreshLoggedStatus.bind(this)}
              saveLoggedUser={this.saveLoggedUser.bind(this)}/>
            <UnauthenticatedRoute
              exact path="/register" name="Register Page" component={Register} appProps={this.state}
              refreshLoggedStatus={this.refreshLoggedStatus.bind(this)}
              saveLoggedUser={this.saveLoggedUser.bind(this)}/>
            <Route exact path="/404" name="Page 404" render={props => <Page404 {...props}/>}/>
            <Route exact path="/500" name="Page 500" render={props => <Page500 {...props}/>}/>
            <AuthenticatedRoute path="/home" name="Home" component={DefaultLayout}
                                appProps={this.state}
                                refreshLoggedStatus={this.refreshLoggedStatus.bind(this)}
                                deleteLoggedUser={this.deleteLoggedUser.bind(this)}
                                loggedUser={this.state.user}/>
            <Route exact path="/" name="Landing" render={props => <Redirect {...props} to="/landing"/>}/>
            <UnauthenticatedRoute exact path="/landing" name="Landing Page" component={Public} appProps={this.state}/>
            {
              this.state.isAuthenticated
                ? null
                : <Route exact path="*" name="Landing" render={props => <Redirect {...props} to="/landing"/>}/>
            }
          </Switch>
        </React.Suspense>
      </HashRouter>
    );
  }
}

export default withCookies(App);
