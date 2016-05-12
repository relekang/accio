/* eslint-disable no-var */
var path = require('path');

var root = path.resolve(__dirname, "../frontend");

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

module.exports.resolve = {
  root,
  alias: {
    '🎨': 'styles/variables.less',
  }
};

module.exports.stylus = {
  use: [require('nib')()], // eslint-disable-line global-require
};
