module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    bower: {
      install: {
        options: {
          verbose: true,
          // grunt-bower-task first downloads the bower packages into
          // `bower_components` then copies the actual needed files into `lib`
          // (because bower pulls from git, it gets tests, docs etc.)
          // therefore this won't work:
          // targetDir: 'bower_components',
          install: true, // This true by default
          // grunt-bower-task doesn't copy actually all scss-files from
          // foundation to the `lib` directory, so don't do it.
          copy: false,   // This true by default
          layout: 'byComponent'
        }
      }
    },

    sass: {
      options: {
        includePaths: ['bower_components/foundation/scss']
      },
      dist: {
        options: {
          //outputStyle: 'compressed'
        },
        files: {
          'global_change_lab/static/global_change_lab/css/app.css': [
            'scss/app.scss'
          ]
        }
      }
    },
    // processhtml: {
    //   dist: {
    //     files: {
    //       '/tmp/global_change_lab/1.html': ['http://localhost:8000/']
    //     }
    //   }
    // },
    uncss: {
      dist: {
        options: {
          urls: ['http://localhost:8000']
        },
        files: {
          'css/uncss.css': []
          }
        }
    },

    cssmin: {
      dist: {
        files: {
          'global_change_lab/static/global_change_lab/css/app.min.css': [ 'global_change_lab/static/global_change_lab/css/app.css' ]
        }
      }
    },

    copy: {
      main: {
        files: [
          {
            src:   'bower_components/jquery/jquery.min.js',
            dest: 'global_change_lab/static/jquery.min.js',
            filter: 'isFile',
          },
          {
            src:          'bower_components/foundation/js/foundation.min.js',
            dest: 'global_change_lab/static/foundation/js/foundation.min.js',
            filter: 'isFile',
          },
          {
            src:          'bower_components/foundation/js/foundation/foundation.dropdown.js',
            dest: 'global_change_lab/static/foundation/js/foundation/foundation.dropdown.js',
            filter: 'isFile',
          },
          {
            src:          'bower_components/jquery-form/jquery.form.js',
            dest: 'global_change_lab/static/jquery-form/jquery.form.js',
            filter: 'isFile',
          },
          {
            src:       'bower_components/jqueryui/ui/minified/jquery.ui.core.min.js',
            dest: 'global_change_lab/static/jqueryui/jquery.ui.core.min.js',
            filter: 'isFile',
          },
          {
            src:       'bower_components/jqueryui/ui/minified/jquery.ui.widget.min.js',
            dest: 'global_change_lab/static/jqueryui/jquery.ui.widget.min.js',
            filter: 'isFile',
          },
          {
            src:       'bower_components/jqueryui/ui/minified/jquery.ui.mouse.min.js',
            dest: 'global_change_lab/static/jqueryui/jquery.ui.mouse.min.js',
            filter: 'isFile',
          },
          {
            src:       'bower_components/jqueryui/ui/jquery.ui.sortable.js',
            //src: 'bower_components/jqueryui/ui/minified/jquery.ui.sortable.min.js',
            dest: 'global_change_lab/static/jqueryui/jquery.ui.sortable.js',
            filter: 'isFile',
          },
          {
            src: 'bower_components/backbone.collectionView/dist/backbone.collectionView.min.js',
            dest:            'global_change_lab/static/backbone/backbone.collectionView.min.js',
            filter: 'isFile',
          },
          {
            src:  'bower_components/medium-editor/dist/js/medium-editor.min.js',
            dest: 'global_change_lab/static/medium-editor/medium-editor.min.js',
            filter: 'isFile',
          },
          {
            src: 'bower_components/medium-editor/dist/css/medium-editor.css',
            dest: 'global_change_lab/static/medium-editor/medium-editor.css',
            filter: 'isFile',
          }
        ]
      }
    },

    watch: {
      // LiveReload when updating django templates
      django_templates: {
        files: [
          'skills/templates/*/*.html',
          'skills/templates/*/*/*.html',
          'global_change_lab/templates/*.html',
          'global_change_lab/templates/*/*.html',
          'global_change_lab/templates/*/*/*.html',
        ],
        options: {
          livereload: true
        }
      },

      // Compile and LiveReload when updating SASS
      sass: {
        files: 'scss/*.scss',
        tasks: ['sass'],
        options: {
          livereload: true
        }
      }
    }
  });

  // The difference between `grunt-sass` and `grunt-contrib-sass` is that
  // `grunt-contrib-sass` uses the ruby gem, whereas `grunt-sass` uses `node-sass`
  // which is a SASS compiler written in Javascript (as a node module).
  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-uncss');
  grunt.loadNpmTasks('grunt-processhtml');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-bower-task');

  // grunt.registerTask('build', ['sass', 'processhtml', 'uncss']);
  grunt.registerTask('build', ['bower', 'sass', 'copy']);
  // grunt.registerTask('default', ['build','watch']);
  grunt.registerTask('default', ['build']);
}
