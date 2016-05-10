/* eslint-disable no-var */
var _ = require('lodash');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var base = require('./base');

module.exports = {
  devtool: 'source-map',
  entry: base.entry,
  output: base.output,
  module: {
    loaders: _.concat(base.loaders, [
      {
        test: /\.styl$/,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader!stylus-loader'),
      },
    ]),
  },
  stylus: base.stylus,
  plugins: [
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production'),
      },
    }),
    new webpack.DefinePlugin({ __DEV__: false }),
    // new webpack.optimize.UglifyJsPlugin({compressor: { warnings: false }}),
    new ExtractTextPlugin('[name].css'),
  ],
};
