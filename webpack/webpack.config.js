const ExtractTextPlugin = require('extract-text-webpack-plugin');
const SpritesmithPlugin = require('webpack-spritesmith');


module.exports = {
  entry: [
    './app/img/preview.png',
    './app/richpreview.scss',
    './app/richpreview.js',
  ],
  output: {
    filename: 'richpreview.js',
    library: 'richpreview',
    libraryExport: 'default',
    libraryTarget: 'umd',
    path: `${__dirname}/../src/collective/behavior/richpreview/browser/static`,
    pathinfo: true,
    publicPath: '++resource++collective.behavior.richpreview/',
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
      use: 'babel-loader',
    }, {
      test: /\.scss$/,
      use: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: [
          'css-loader',
          'postcss-loader',
          'sass-loader'
        ]
      }),
    }, {
      test: /.*\.(gif|png|jpe?g)$/i,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: '[path][name].[ext]',
            context: 'app/',
          }
        },
        {
          loader: 'image-webpack-loader',
          query: {
            mozjpeg: {
              progressive: true,
            },
            pngquant: {
              quality: '65-90',
              speed: 4,
            },
            gifsicle: {
              interlaced: false,
            },
            optipng: {
              optimizationLevel: 7,
            }
          }
        }
      ]
    }, {
      test: /\.svg/,
      exclude: /node_modules/,
      use: 'svg-url-loader',
    }]
  },
  devtool: 'source-map',
  plugins: [
    new ExtractTextPlugin({
      filename: 'richpreview.css',
      allChunks: true
    }),
    new SpritesmithPlugin({
      src: {
        cwd: 'app/sprite',
        glob: '*.png',
      },
      target: {
        image: 'app/img/sprite.png',
        css: 'app/scss/_sprite.scss',
      },
      apiOptions: {
        cssImageRef: './img/sprite.png',
      }
    }),
  ]
}
