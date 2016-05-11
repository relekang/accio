export const RECEIVE_PROJECT = 'RECEIVE_PROJECT';
export const receiveProject = project => ({ type: RECEIVE_PROJECT, data: project });

export function fetchProject(id) {
  return (dispatch, getState, { api }) =>
    api.get('/projects', { id })
      .then(values => dispatch(receiveProject(values)))
      .catch(error => { throw error; });
}

export function deployProject(id, data) {
  return (dispatch, getState, { api }) =>
    api.post(`/projects/${id}/deploy/`, data)
      .then(() => fetchProject(id)(dispatch, getState, { api }))
      .catch(error => { throw error; });
}
