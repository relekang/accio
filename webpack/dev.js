/* eslint-disable no-var */
var _ = require('lodash');
var webpack = require('webpack');

var base = require('./base');

module.exports = {
  devtool: 'cheap-module-eval-source-map',
  entry: _.concat(['webpack-hot-middleware/client?reload=true'], base.entry),
  module: {
    loaders: _.concat(base.loaders, [
      {
        test: /\.styl$/,
        loader: 'style-loader!css-loader!stylus-loader',
      },
    ]),
  },
  output: base.output,
  stylus: base.stylus,
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('development'),
      },
    }),
  ],
};
