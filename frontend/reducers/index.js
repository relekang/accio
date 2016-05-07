import { combineReducers } from 'redux';
import { routerReducer as routing } from 'react-router-redux';

import { projects } from './projects';
import { user } from './user';

export default combineReducers({
  routing,
  projects,
  user,
});
