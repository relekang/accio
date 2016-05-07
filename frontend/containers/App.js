import _ from 'lodash';
import React from 'react';
import { connect } from 'react-redux';
import { IndexLink } from 'react-router';

import UserMenu from '../components/UserMenu';

export const App = ({ children, user }) => (
  <div className="app-container">
    <div className="header">
      <div className="container">
        <UserMenu {...user } />
        <IndexLink to="/">ACCIO</IndexLink>
      </div>
    </div>
    <div className="content">
      <div className="container">
        {children}
      </div>
    </div>
    <div className="footer">
      <div className="container flex flex--center">
        <div className="flex--1">
          {_.get(user, 'isAuthenticated') && <a href="/logout/">Logout</a>}<br />
        </div>
      </div>
    </div>
  </div>
);

App.propTypes = {
  children: React.PropTypes.any,
  user: React.PropTypes.object.isRequired,
};

export default connect(state => ({
  user: state.user,
}))(App);
