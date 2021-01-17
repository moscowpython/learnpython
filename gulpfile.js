'use strict';

const gulp = require('gulp'),
    sass = require('gulp-sass'),
    csso = require('gulp-csso'),
    sourcemaps = require('gulp-sourcemaps'),
    merge = require('merge-stream'),
    through2 = require('through2'),
    scss = {
        'landing_page/mainpage/static/new-design/css/**/*.scss': 'landing_page/mainpage/static/new-design/css'
    };

gulp.task('scss', () => {
    return merge(Object.keys(scss).map(source => {
        let destination = scss[source];

        return gulp.src(source)
            .pipe(sourcemaps.init())
            .pipe(sass().on('error', sass.logError))
            .pipe(csso({restructure: false, comments: 'exclamation'}))
            .pipe(sourcemaps.write('.'))
            .pipe(through2.obj(function(file, enc, cb) {
                let date = new Date();

                file.stat.atime = date;
                file.stat.mtime = date;

                cb(null, file);
            }))
            .pipe(gulp.dest(destination));
    }));
});

gulp.task('scss:watch', gulp.series('scss', () => {
    gulp.watch(Object.keys(scss), gulp.series('scss'));
}));

gulp.task('default', gulp.series('scss:watch'));
