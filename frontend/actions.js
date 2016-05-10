import { get } from './service';

export const RECEIVE_PROJECT = 'RECEIVE_PROJECT';
const receiveProject = project => ({ type: RECEIVE_PROJECT, data: project });

export function fetchProject(id) {
  return dispatch =>
    get('/projects', { id })
      .then(values => dispatch(receiveProject(values)))
      .catch(error => { throw error; });
}
