import moment from 'moment';
import React, { PropTypes } from 'react';
import { get } from 'lodash';

import './ProjectDetails.styl';

const ProjectDetails = ({ project }) => (
  <div className="ProjectDetails text-center">
    <h1>{get(project.owner, 'name')} / {project.name}</h1>
    <h2>Last deployment</h2>
    {project.lastDeploy &&
      <em>{get(project.lastDeploy, 'shortRef')}
      -
      {moment(get(project.lastDeploy, 'finishedAt')).fromNow()}</em>
    }
  </div>
);

ProjectDetails.propTypes = {
  project: PropTypes.object.isRequired,
};

export default ProjectDetails;
