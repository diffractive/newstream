var gulp = require('gulp');
const { watch } = require('gulp');
var sass = require('gulp-sass');
var postcss = require('gulp-postcss');
var rename = require('gulp-rename');
const cleanCSS = require('gulp-clean-css');
const through2 = require('through2');
const srcpath = 'newstream/static/scss/main.scss';
const destpath = 'newstream/static/css/';

function css() {
  return gulp.src(srcpath)
    .pipe(sass().on('error', sass.logError))
    .pipe(postcss([
      require('tailwindcss'),
      require('autoprefixer'),
    ]))
    .pipe(cleanCSS({ compatibility: 'ie8' }))
    .pipe(through2.obj(function (file, enc, cb) {
      let date = new Date();
      file.stat.atime = date;
      file.stat.mtime = date;
      cb(null, file);
    }))
    .pipe(rename('main_1_4.css'))
    .pipe(gulp.dest(destpath))
}

exports.default = css
exports.watch = function () {
  // You can use a single task
  watch(srcpath, css);
};
