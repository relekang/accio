import './styles/main.styl'
import 'babel-polyfill'
import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { Router, browserHistory } from 'react-router'
import { syncHistoryWithStore } from 'react-router-redux'

import Routes from './routes'
import store from './store'
import DevTools from './containers/dev_tools'

const user = Object.assign({}, window.user)

if (!user.isAnonymous) {
  localStorage.setItem('betaAccess', 'true')
}

const history = syncHistoryWithStore(browserHistory, store)


render(
  <Provider store={store}>
    <div>
      <Router history={history}>
        {Routes}
      </Router>
      {__DEV__ && <DevTools />}
    </div>
  </Provider>,
  document.getElementById('app')
)
