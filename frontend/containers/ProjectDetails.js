import { connect } from 'react-redux';
import { find } from 'lodash';

import { fetchProject } from '../actions';
import ProjectDetails from '../components/ProjectDetails';

function mapStateToProps({ projects, user }, { params }) {
  const project = find(projects, ({ owner, name }) =>
    owner.name === params.owner && name === params.name
  );
  return { project, user };
}

export default connect(mapStateToProps, { fetchProject })(ProjectDetails);
