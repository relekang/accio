/* eslint-disable no-var */
/* eslint-disable no-console */
var express = require('express')
var webpack = require('webpack')
var httpProxyMiddleware = require('http-proxy-middleware')

var config = require('./webpack/dev')

var app = express()
var compiler = webpack(config)

app.use(require('webpack-dev-middleware')(compiler, {
  noInfo: true,
  publicPath: config.output.publicPath,
}))

app.use(require('webpack-hot-middleware')(compiler))
app.use(httpProxyMiddleware('http://localhost:8000/**'))

app.listen(3000, 'localhost', err => {
  if (err) {
    console.log(err)
    return
  }

  console.log('Listening at http://localhost:3000')
})
