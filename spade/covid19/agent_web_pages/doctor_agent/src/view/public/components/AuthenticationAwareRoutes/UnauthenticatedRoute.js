import React from 'react';
import {Redirect, Route} from 'react-router-dom';

export default function UnauthenticatedRoute({component: C, appProps, ...rest}) {
  const redirect = queryString("redirect");
  return (
    <Route
      {...rest}
      render={props => !appProps.isAuthenticated
        ? <C {...rest} {...props} {...appProps} />
        : <Redirect to={redirect === "" || redirect === null ? "/home" : redirect}/>}
    />
  );
}

function queryString(name, url = window.location.href) {
  name = name.replace(/[[]]/g, "\\$&");

  const regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)", "i");
  const results = regex.exec(url);

  if (!results) {
    return null;
  }
  if (!results[2]) {
    return "";
  }

  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

