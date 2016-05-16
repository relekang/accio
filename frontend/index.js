import './styles/main.styl';
import 'babel-polyfill';
import React from 'react';
import { cloneDeep } from 'lodash';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { Router, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';

import Routes from './routes';
import DevTools from './containers/DevTools';
import configureStore from './store_creator';

const user = Object.assign({}, window.user);
const projects = cloneDeep(window.projects);
export const store = configureStore(browserHistory, {
  user,
  projects,
});

const history = syncHistoryWithStore(browserHistory, store);

render(
  <Provider store={store}>
    <div>
      <Router history={history} routes={Routes} />
      {process.env.NODE_ENV !== 'production' && <DevTools />}
    </div>
  </Provider>,
  document.getElementById('app')
);
