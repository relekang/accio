import moment from 'moment';
import React, { PropTypes } from 'react';
import { get, map } from 'lodash';

import './ProjectDetails.styl';

const ProjectDetails = ({ project }) => (
  <div className="ProjectDetails">
    <h1>{get(project.owner, 'name')} / {project.name}</h1>
    <h2>Last deployment</h2>
    {project.lastDeploy &&
      <em>{get(project.lastDeploy, 'shortRef')}
      -
      {moment(get(project.lastDeploy, 'finishedAt')).fromNow()}</em>
    }
    {map(project.lastDeploy.taskResults, task => (
      <div>
        <h3>{task.taskType}</h3>
        <pre><code>{JSON.stringify(task.result, null, 2)}</code></pre>
      </div>
    ))}
  </div>
);

ProjectDetails.propTypes = {
  project: PropTypes.object.isRequired,
};

export default ProjectDetails;
