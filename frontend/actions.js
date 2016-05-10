export const RECEIVE_PROJECT = 'RECEIVE_PROJECT';
export const receiveProject = project => ({ type: RECEIVE_PROJECT, data: project });

export function fetchProject(id) {
  return (dispatch, api) =>
    api.get('/projects', { id })
      .then(values => dispatch(receiveProject(values)))
      .catch(error => { throw error; });
}
