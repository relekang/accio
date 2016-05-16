import test from 'ava';
import { keys } from 'lodash';

import createStore from '../store_creator';

test('configureStore(browserHistory, initialState) should return a store', t => {
  const store = createStore({}, { user: { username: 'dumbledore' } });

  t.deepEqual(keys(store), ['dispatch', 'subscribe', 'getState', 'replaceReducer', 'liftedStore']);
  t.deepEqual(store.getState().user, { username: 'dumbledore' });
});
