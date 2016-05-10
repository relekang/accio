import moment from 'moment';
import React, { Component, PropTypes } from 'react';
import { get, isEmpty, map } from 'lodash';

import './ProjectDetails.styl';

export default class ProjectDetails extends Component {

  componentDidMount() {
    this.interval = window.setInterval(() => {
      if (this.props.project.lastDeploy && this.props.project.lastDeploy.finishedAt === null) {
        this.props.fetchProject(this.props.project.id);
      }
    }, 500);
  }

  componentWillUnmount() {
    if (this.interval) {
      window.clearInterval(this.interval);
    }
  }

  render() {
    const { lastDeploy } = this.props.project;
    return (
      <div className="this.props.projectDetails">
        <h1>{get(this.props.project.owner, 'name')} / {this.props.project.name}</h1>
        {lastDeploy &&
          <div>
            <h2>Last deployment</h2>
            {lastDeploy && <em>
              {get(lastDeploy, 'shortRef')} - {moment(get(lastDeploy, 'finishedAt')).fromNow()}
            </em>}
            {map(lastDeploy.taskResults, (task, i) => <TaskResult key={i} {...task} />)}
          </div>
        }
      </div>
    );
  }
}

ProjectDetails.propTypes = {
  fetchProject: PropTypes.func.isRequired,
  project: PropTypes.object.isRequired,
};

const TaskResult = ({ commands, taskType, result }) => {
  let keys = Object.keys(result);
  if (!isEmpty(commands) && !result.hasOwnProperty('ssh')) {
    keys = commands;
  }

  return (
    <div>
      <h3>{taskType}</h3>
      <code className="overflow-x">
        {map(keys, key => {
          const { error, stdout, exitCode } = result[key];
          return (
            <div key={taskType + key} className="padding">
              $ <strong>{key}</strong> <span title="Exit code">({exitCode})</span>
              <pre>{stdout || error}</pre>
            </div>
          );
        })}
      </code>
    </div>
  );
};

TaskResult.propTypes = {
  commands: PropTypes.array.isRequired,
  taskType: PropTypes.string.isRequired,
  result: PropTypes.object.isRequired,
};
