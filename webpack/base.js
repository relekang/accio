/* eslint-disable no-var */
var path = require('path');

module.exports.entry = [
  './frontend/index',
];

module.exports.output = {
  path: path.join(__dirname, '..', 'static'),
  filename: 'bundle.js',
  publicPath: '/static/',
};

module.exports.loaders = [
  {
    test: /\.js$/,
    loader: 'babel-loader',
    exclude: /node_modules/,
  },
  {
    test: /\.(png|jpg|jpeg|svg)$/,
    loader: 'url-loader?limit=8192',
  },
];

module.exports.stylus = {
  use: [require('nib')()], // eslint-disable-line global-require
};
