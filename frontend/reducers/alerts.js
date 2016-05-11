import { findIndex } from 'lodash';
import { ADD_ALERT, REMOVE_ALERT } from '../actions';

export function alerts(state = [], action) {
  let index;
  switch (action.type) {
    case ADD_ALERT:
      return [...state, action.data];

    case REMOVE_ALERT:
      index = findIndex(state, { id: action.data.id });
      if (index !== -1) {
        return [...state.splice(0, index), ...state.splice(index + 1)];
      }
      return state;

    default:
      return state;
  }
}
