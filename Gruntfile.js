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
          },
          {
            src: 'bower_components/medium-editor/dist/css/medium-editor.css',
            dest: 'global_change_lab/static/medium-editor/medium-editor.css',
            filter: 'isFile',
          },
        ]
      }
    },

    uglify: {
      // The bare minimum for the site to function (front-page)
      options: {
        sourceMap: true,
        sourceMapIncludeSources: true,
      },
      user: {
        files: {
          'global_change_lab/static/global_change_lab/js/user.min.js': [
            // 'bower_components/jquery/dist/jquery.js',                                // 82 kb
            'bower_components/jquery.cookie/jquery.cookie.js',                          //  3 kb
            'bower_components/foundation/js/foundation.js',                             // 16 kb
            'bower_components/foundation/js/foundation/foundation.dropdown.js',         //  7 kb
          ]
        }
      },
      // The needed things to view a training bit
      trainingbit_view: {
        files: {
          'global_change_lab/static/global_change_lab/js/trainingbit_view.min.js': [
            'bower_components/underscore/underscore.js',
            'bower_components/backbone/backbone.js',
            'bower_components/backbone.collectionView/dist/backbone.collectionView.js',
          ]
        }
      },
      // The needed things to upload images the "AJAX/HTML5"-way
      fileupload: {
        files: {
          'global_change_lab/static/global_change_lab/js/fileupload.min.js': [
            'bower_components/jqueryui/ui/jquery.ui.core.js',
            'bower_components/jqueryui/ui/jquery.ui.widget.js',
            'bower_components/jquery-file-upload/js/jquery.iframe-transport.js',
            'bower_components/jquery-file-upload/js/jquery.fileupload.js',
          ]
        }
      },
      // For editing training bits and using the trainer interface
      trainer: {
        files: {
          'global_change_lab/static/global_change_lab/js/trainer.min.js': [
            'bower_components/listjs/dist/list.js',
            'bower_components/medium-editor/dist/js/medium-editor.js',
            'bower_components/jqueryui/ui/jquery.ui.core.js',
            'bower_components/jqueryui/ui/jquery.ui.widget.js',
            'bower_components/jqueryui/ui/jquery.ui.mouse.js',
            'bower_components/jqueryui/ui/jquery.ui.sortable.js',
            'bower_components/jquery-throttle-debounce/jquery.ba-throttle-debounce.js',
            'bower_components/jquery-form/jquery.form.js',
            'bower_components/offline/offline.min.js',
          ]
        }
      }
    },

    watch: {
      // LiveReload when updating django templates and views.py
      django_templates: {
        files: [
          'skills/views.py',
          'skills/templates/*/*.html',
          'skills/templates/*/*/*.html',
          'global_change_lab/views.py',
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
  grunt.loadNpmTasks('grunt-contrib-uglify');

  // grunt.registerTask('build', ['sass', 'processhtml', 'uncss']);
  grunt.registerTask('build', ['bower', 'sass', 'uglify', 'copy']);
  // grunt.registerTask('default', ['build','watch']);
  grunt.registerTask('default', ['build']);
}
