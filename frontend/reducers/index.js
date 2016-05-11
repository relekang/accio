import { combineReducers } from 'redux';
import { routerReducer as routing } from 'react-router-redux';

import { alerts } from './alerts';
import { projects } from './projects';
import { user } from './user';

export default combineReducers({
  alerts,
  routing,
  projects,
  user,
});
