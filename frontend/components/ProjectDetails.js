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
        {map(task.result, ({ error, stdout, exitCode }, key) => (
          <code>
            $ <strong>{key}</strong> <span title="Exit code">({exitCode})</span>
            <pre>{stdout || error}</pre>
          </code>
        ))}
      </div>
    ))}
  </div>
);

ProjectDetails.propTypes = {
  project: PropTypes.object.isRequired,
};

export default ProjectDetails;
