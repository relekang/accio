import { applyMiddleware, compose, createStore } from 'redux';
import { routerMiddleware } from 'react-router-redux';
import thunkMiddleware from 'redux-thunk';
import createLogger from 'redux-logger';

import DevTools from './containers/DevTools';
import reducers from './reducers';
import * as api from './api';

const loggerMiddleware = createLogger();

export default function configureStore(browserHistory, initialState) {
  let middlewares = [
    thunkMiddleware.withExtraArgument({ api }),
    routerMiddleware(browserHistory),
  ];

  if (process.env.NODE_ENV !== 'production') {
    middlewares = [
      ...middlewares,
      loggerMiddleware,
    ];
  }

  let storeEnhancers = [applyMiddleware(...middlewares)];

  if (process.env.NODE_ENV !== 'production') {
    storeEnhancers = [...storeEnhancers, DevTools.instrument()];
  }

  const finalCreateStore = compose(...storeEnhancers)(createStore);
  return finalCreateStore(reducers, initialState);
}
