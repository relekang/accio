import React from 'react';
import { get } from 'lodash';
import { IndexRoute, Route } from 'react-router';

import App from './containers/App';

function getContainer(name) {
  return (location, callback) => {
    require.ensure([], require => {
      callback(null, require(`./containers/${name}`).default);
    });
  };
}

function loginRequired(nextState, replace) {
  if (!get(window.user, 'isAuthenticated')) {
    replace({ pathname: '/' });
  }
}

export default (
  <Route path="/" component={App}>
    <IndexRoute getComponent={getContainer('LandingPage')} />
    <Route
      path="projects/:owner/:name"
      getComponent={getContainer('ProjectDetails')}
      onEnter={loginRequired}
    />
    <Route path="*" getComponent={getContainer('NotFound')} onEnter={loginRequired} />
  </Route>
);
