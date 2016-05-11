import { assign } from 'lodash';
export const RECEIVE_PROJECT = 'RECEIVE_PROJECT';
export const ADD_ALERT = 'ADD_ALERT';
export const REMOVE_ALERT = 'REMOVE_ALERT';

export const receiveProject = project => ({ type: RECEIVE_PROJECT, data: project });
export const removeAlert = id => ({ type: REMOVE_ALERT, data: { id } });
export const addAlert = (dispatch, alert) => {
  const id = alert.id || new Date().getTime();
  setTimeout(() => dispatch(removeAlert(id)), alert.timeout || 1000);
  return { type: ADD_ALERT, data: assign({ id, type: 'info' }, alert) };
};

export function fetchProject(id) {
  return (dispatch, getState, { api }) =>
    api.get('/projects', { id })
      .then(values => dispatch(receiveProject(values)))
      .catch(error => { throw error; });
}

export function deployProject(id, data) {
  return (dispatch, getState, { api }) => {
    const alertId = new Date().getTime() + (10000 * id);
    dispatch(addAlert(dispatch, { message: 'Starting deploy', id: alertId }));
    return api.post(`/projects/${id}/deploy/`, data)
      .then(() => {
        dispatch(removeAlert(alertId));
        dispatch(addAlert(dispatch, { type: 'success', message: 'Started deploy' }))
      })
      .then(() => fetchProject(id)(dispatch, getState, { api }))
      .catch(error => {
        dispatch(removeAlert(alertId));
        dispatch(addAlert(dispatch, {
          type: 'error',
          message: 'Could not start deploy',
          timeout: 5000,
        }));
        throw error;
      });
  };
}
