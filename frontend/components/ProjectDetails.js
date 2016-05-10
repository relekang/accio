import moment from 'moment';
import React, { Component, PropTypes } from 'react';
import { get, map } from 'lodash';

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
    return (
      <div className="this.props.projectDetails">
        <h1>{get(this.props.project.owner, 'name')} / {this.props.project.name}</h1>
        {this.props.project.lastDeploy &&
          <div>
            <h2>Last deployment</h2>
            {this.props.project.lastDeploy &&
              <em>{get(this.props.project.lastDeploy, 'shortRef')}
              -
              {moment(get(this.props.project.lastDeploy, 'finishedAt')).fromNow()}</em>
            }
            {map(this.props.project.lastDeploy.taskResults, task => (
              <div>
                <h3>{task.taskType}</h3>
                <code className="overflow-x">
                  {map(task.result, ({ error, stdout, exitCode }, key) => (
                    <div className="padding">
                      $ <strong>{key}</strong> <span title="Exit code">({exitCode})</span>
                      <pre>{stdout || error}</pre>
                    </div>
                  ))}
                </code>
              </div>
            ))}
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
