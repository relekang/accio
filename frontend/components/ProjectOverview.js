import moment from 'moment';
import React, { PropTypes } from 'react';
import { get, map } from 'lodash';

import { Deployment } from '../propTypes';
import './ProjectOverview.styl';

const ProjectOverview = ({ projects }) => (
  <div className="ProjectOverview">
    <h2>Projects</h2>
    {map(projects, project =>
      <Project key={project.id} {...project} />)
    }
  </div>
);

ProjectOverview.propTypes = {
  projects: PropTypes.arrayOf(PropTypes.object).isRequired,
};

export default ProjectOverview;

export const Project = ({ owner, name, lastDeploy }) => (
  <div className="Project text-center">
    <h3>{get(owner, 'name')}/{name}</h3>
    {lastDeploy &&
      <em>{get(lastDeploy, 'shortRef')}
      -
      {moment(get(lastDeploy, 'finishedAt')).fromNow()}</em>
    }
  </div>
);

Project.propTypes = {
  owner: PropTypes.object.isRequired,
  name: PropTypes.string.isRequired,
  lastDeploy: PropTypes.shape(Deployment),
};
