import { map } from 'lodash';
import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';

import './Alerts.styl';

function Alerts({ alerts }) {
  return (
    <div className="Alerts">
      <ReactCSSTransitionGroup
        transitionName="Alert"
        transitionEnterTimeout={500}
        transitionLeaveTimeout={300}
      >
        {map(alerts, (alert, i) => <Alert key={i} {...alert} />)}
      </ReactCSSTransitionGroup>
    </div>
  );
}

export default connect(({ alerts }) => ({ alerts }))(Alerts);

function Alert({ message, type }) {
  return <div className={`Alert ${type}`}><span>{message}</span></div>;
}

Alerts.propTypes = {
  alerts: PropTypes.shape(Alert.propTypes),
};

Alerts.propTypes = {
  alerts: PropTypes.arrayOf(PropTypes.shape(Alert.propTypes)),
};
