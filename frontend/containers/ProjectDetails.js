import { connect } from 'react-redux';
import { find } from 'lodash';

import { fetchProject } from '../actions';
import havePropOr404 from '../components/prop_or_404';
import ProjectDetails from '../components/ProjectDetails';

function mapStateToProps({ projects, user }, { params }) {
  const project = find(projects, ({ owner, name }) =>
    owner.name === params.owner && name === params.name
  );
  return { project, user };
}

export default connect(mapStateToProps, { fetchProject })(havePropOr404('project', ProjectDetails));
