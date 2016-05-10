import { findIndex } from 'lodash';
import { RECEIVE_PROJECT } from '../actions';

export function projects(state = [], { type, data }) {
  let index;
  switch (type) {
    case RECEIVE_PROJECT:
      index = findIndex(state, ['id', data.id]);
      if (index !== -1) {
        return [...state.slice(0, index), data, ...state.slice(index + 1)];
      }
      return [...state, data];

    default:
      return state;
  }
}
