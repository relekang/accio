import test from 'ava';
import { noop } from 'lodash';

import { RECEIVE_PROJECT, receiveProject, fetchProject } from '../actions';

test('receiveProject should return object with type and data', t => {
  t.deepEqual(receiveProject({ id: 42 }), { type: RECEIVE_PROJECT, data: { id: 42 } });
});

test('fetchProject should dispatch object', t => {
  t.plan(1);
  const apiMock = { get: (path, { id }) => Promise.resolve({ id }) };
  const dispatch = action => t.deepEqual(action, receiveProject({ id: 42 }));
  return fetchProject(42)(dispatch, apiMock);
});

test('fetchProject should throw error', t => {
  const apiMock = { get: () => Promise.reject(new Error('Something failed')) };
  t.throws(fetchProject(42)(noop, apiMock));
});
