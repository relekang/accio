import React from 'react';
import { get } from 'lodash';
import { IndexRoute, Route } from 'react-router';

import App from './containers/App';

function getLandingPage(name) {
  return ;
}

function loginRequired(nextState, replace) {
  if (!get(window.user, 'isAuthenticated')) {
    replace({ pathname: '/' });
  }
}

export default (
  <Route path="/" component={App}>
    <IndexRoute
      getComponent={(location, callback) => {
        require.ensure([], require => {
          callback(null, require('./containers/LandingPage').default);
        });
      }}
    />
    <Route
      path="projects/:owner/:name"
      getComponent={(location, callback) => {
        require.ensure([], require => {
          callback(null, require('./containers/ProjectDetails').default);
        });
      }}
      onEnter={loginRequired}
    />
    <Route
      path="*"
      getComponent={(location, callback) => {
        require.ensure([], require => {
          callback(null, require('./containers/NotFound').default);
        });
      }}
      onEnter={loginRequired}
    />
  </Route>
);
