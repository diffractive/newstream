var gulp = require('gulp');
const { watch } = require('gulp');
var sass = require('gulp-sass');
var postcss = require('gulp-postcss');
const srcpath = 'omp/static/scss/main.scss';
const destpath = 'omp/static/css/';

function css() {
    return gulp.src(srcpath)
        .pipe(sass().on('error', sass.logError))
        .pipe(postcss([
            require('tailwindcss'),
            require('autoprefixer'),
        ]))
        .pipe(gulp.dest(destpath))
}

exports.default = css
exports.watch = function() {
  // You can use a single task
  watch(srcpath, css);
};
