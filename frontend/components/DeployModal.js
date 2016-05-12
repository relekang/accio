import moment from 'moment';
import React, { Component, PropTypes } from 'react';
import { get, isEmpty, keys, map } from 'lodash';

import './ProjectDetails.styl';
import Modal from './Modal';
import Spinner from './Spinner';

export default class ProjectDetails extends Component {
  constructor(props, context) {
    super(props, context);
    this.onDeploy = this.onDeploy.bind(this);
  }

  render() {
    return (
      <Modal>

      </Modal>
    );
  }
}
