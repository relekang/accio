import React, { PropTypes } from 'react';
import { connect } from 'react-redux';

import ProjectOverview from '../components/ProjectOverview';

export const LandingPage = ({ projects, user }) => (
  <div className="LandingPage">
    {user.isAuthenticated ?
      <ProjectOverview projects={projects} />
    :
      <p className="lead text-center">Seems like you are not logged in</p>
    }
  </div>
);

LandingPage.propTypes = {
  projects: PropTypes.arrayOf(PropTypes.object).isRequired,
  user: PropTypes.object.isRequired,
};

export default connect(({ projects, user }) => ({ projects, user }))(LandingPage);
