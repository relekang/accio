import test from 'ava';
import freeze from 'deep-freeze';

import { user } from '../user';

test('reducers(user) should return state for unknown action', t => {
  const state = freeze([{ id: 42 }]);
  t.is(user(state, {}), state);
});
