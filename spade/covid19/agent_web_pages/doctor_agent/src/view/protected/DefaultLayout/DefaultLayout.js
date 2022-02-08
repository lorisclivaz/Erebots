import React, {Component, Suspense} from 'react';
import * as router from 'react-router-dom';
import {Redirect, Route, Switch} from 'react-router-dom';
import {Container} from 'reactstrap';
import {logOut} from "../../../controller/ServerApi";

import {
  AppBreadcrumb2 as AppBreadcrumb,
  AppFooter,
  AppHeader,
  AppSidebar,
  AppSidebarFooter,
  AppSidebarForm,
  AppSidebarHeader,
  AppSidebarMinimizer,
  AppSidebarNav2 as AppSidebarNav,
} from '@coreui/react';
// sidebar nav config
import navigation from '../../../_nav';
// routes config
import routes from '../../../routes';
import {createLoading} from "../../../utils/DataLoadingUtils";


const DefaultFooter = React.lazy(() => import('./DefaultFooter'));
const DefaultHeader = React.lazy(() => import('./DefaultHeader'));

class DefaultLayout extends Component {

  async signOut(e) {
    e.preventDefault();
    await logOut();
    this.props.deleteLoggedUser();
    this.props.refreshLoggedStatus()
  }

  render() {
    // require('../../utils/logging').log("DefaultLayout.js","props : ", this.props);
    // log("DefaultLayout state : ", this.state);
    return (
      <div className="app">
        <AppHeader fixed>
          <Suspense fallback={createLoading({pt: 1, position: 'center'})}>
            <DefaultHeader onLogout={e => this.signOut(e)} loggedUser={this.props.loggedUser}/>
          </Suspense>
        </AppHeader>
        <div className="app-body">
          <AppSidebar fixed display="lg">
            <AppSidebarHeader/>
            <AppSidebarForm/>
            <Suspense fallback={this.loading}>
              <AppSidebarNav navConfig={navigation} location={this.props.location} router={router}/>
            </Suspense>
            <AppSidebarFooter/>
            <AppSidebarMinimizer/>
          </AppSidebar>
          <main className="main">
            <AppBreadcrumb appRoutes={routes} router={router}/>
            <Container fluid>
              <Suspense fallback={createLoading({pt: 1, position: 'center'})}>
                <Switch>
                  {routes.map((route, idx) => {
                    return route.component ? (
                      <Route
                        key={idx}
                        path={route.path}
                        exact={route.exact}
                        name={route.name}
                        render={props => (
                          <route.component {...props} />
                        )}/>
                    ) : null;
                  })}
                  <Redirect from="/home" to="/home/dashboard"/>
                </Switch>
              </Suspense>
            </Container>
          </main>
          {/* DISABLED ASIDE FOR NOW */}
          {/*<AppAside fixed>*/}
          {/*  <Suspense fallback={createLoading({pt: 1, position: 'center'})}>*/}
          {/*    <DefaultAside/>*/}
          {/*  </Suspense>*/}
          {/*</AppAside>*/}
        </div>
        <AppFooter>
          <Suspense fallback={createLoading({pt: 1, position: 'center'})}>
            <DefaultFooter/>
          </Suspense>
        </AppFooter>
      </div>
    );
  }
}

export default DefaultLayout;
