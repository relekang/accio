import test from 'ava';

import reducers from '../';

test('combineReducers should not fail', t => {
  t.truthy(reducers);
});
