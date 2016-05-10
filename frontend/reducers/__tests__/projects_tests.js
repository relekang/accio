import test from 'ava';
import freeze from 'deep-freeze';

import { projects } from '../projects';
import { RECEIVE_PROJECT } from '../../actions';

test('reducers(projects) should return state for unknown action', t => {
  const state = freeze([{ id: 42 }]);
  t.is(projects(state, {}), state);
});

test('reducers(projects) should add project if it is not already in state', t => {
  const state = freeze([{ id: 42 }]);
  t.deepEqual(
    projects(state, { type: RECEIVE_PROJECT, data: { id: 1, name: 'accio' } }),
    [{ id: 42 }, { id: 1, name: 'accio' }]
  );
});

test('reducers(projects) should replace project if it is not already in state', t => {
  const state = freeze([{ id: 42, name: 'accio' }]);
  t.deepEqual(
    projects(state, { type: RECEIVE_PROJECT, data: { id: 42 } }),
    [{ id: 42 }]
  );
});
