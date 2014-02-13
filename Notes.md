Bower install via Grunt
-----------------------
In order to install as many packages locally in the project folder, we invoke
bower via grunt (`grunt bower`) instead of doing `bower install` which requires
bower to be installed globally.

There are basically two grunt packages for this (probably more):

* <https://www.npmjs.org/package/grunt-bower>
* <https://github.com/yatskevich/grunt-bower-task>

I chose `grunt-bower-task`, for some reason, don't remember. Doesn't matter,
probably.

Training bit content editor
---------------------------
The text of training bit has support for bold, italics and underline.
There are loads of options:

* [Medium Editor](https://github.com/daviferreira/medium-editor)
* [Pen Editor](http://sofish.github.io/pen/)
* [Hallo.js](https://github.com/bergie/hallo)
* (etch.js)(http://etchjs.com/)
  Actually uses backbone, but it relies on saving. And that simply isn't explained.
  So...
* [Medium.js](http://jakiestfu.github.io/Medium.js/docs/)
  Doesn't have the toolbar so you need to press `Ctrl-B`, `Ctrl-I` etc. for it to
  work.
* [ZenPen](https://github.com/tholman/zenpen)
  A "zen" interface (takes up all of the screen)
* Grande.js


See: <https://www.codersgrid.com/2013/09/04/medium-editor-ui-zenpen-grande-js-and-pen-editor/>

Data model for training bit content
----------------------------------
Training bits consists of a list of different types of widgets (text field,
image, video embed ...) these can be repeated and be in any order.
And this list of widgets must be stored persistently.

The most django-centric solution would be too use
[django-widgy](https://github.com/fusionbox/django-widgy). Here you will have
all the information in the database, and readily available to django, in a
format understood by django.

django-widgy, however doesn't work in Python 3

At the other end of the spectrum of data models we could argue that because we
know the trainer can dynamically add and reorder the parts and the Javascript
handling this must have an internal representation of the widgets. And we could
simply store that (the JSON) as data in a VARCHAR-field.

This would most likely mean that django would not be able to generate static
HTML for the widgets directly, but would need to send the JSON to the page, and
let Javascript output the HTML. To mitigate this problem for computers that hate
Javascript you could use PhantomJS to generate the HTML on the server and pass
that on. The load on the server from PhantomJS could again be alleviated by
setting up a cache with hashes of the JSON as keys and the HTML as values. (So
you don't have to run PhantomJS twice on the same piece of JSON)

Other solution could be using `django-treebeard` to have a list of widgets.
http://codeblow.com/questions/django-how-do-you-model-a-tree-of-heterogeneous-data-types/

Or storing `pickle`d objects in the database.

See: <http://stackoverflow.com/questions/1110153/what-is-the-most-efficent-way-to-store-a-list-in-the-django-models>
For optimizing (automated denormalization): <https://github.com/initcrash/django-denorm/tree/master>

### Conclusion
Having _one_ (canonical) representation of data is something I'm a big fan of.
Since I will _have to have_ a Javascript representation of the training bit this
will be my canonical representation, which will be stored in the database.
The training bits are as such flat "HTML" pages anyway and thus django doesn't
need to know anything about the content. (It's purely a representational problem).
Furthermore there's a one-to-one relationship between a training bit and its
content.

The most immediate danger with this solution is the answers/projects the users
can upload to a training bit. In order to recieve the answer to a training bit,
django has to know what kind of answer it can expect from the training bit: a
picture, a link, a text?

user.is_authenticated in templates
----------------------------------
In order for user information to be available to a template a `RequestContext`
must be passed to it.  The `render()` function does this by default, while
`render_to_response()` does not.  Therefore you should always use `render()`.
See: <https://docs.djangoproject.com/en/1.6/ref/templates/api/#subclassing-context-requestcontext>

Furthermore you need to include `django.contrib.auth.context_processors.auth`
in `TEMPLATE_CONTEXT_PROCESSORS`. This inject a template variable called `user`
into all template contexts. `user` is the object representing the currently
logged in user.  This means you should **not** use the template variable called
`user` as it will override the logged in user object and thing will mess up.
See: <https://docs.djangoproject.com/en/1.6/ref/templates/api/#django-contrib-auth-context-processors-auth>

**TL;DR** Don't name your own template variables `user` and always use
`render()` instead of `render_to_response()`.

Getting south to work
---------------------
DROP currently existing databases:

    > ./manage.py sqlclear global_change_lab skills | psql -U postgres -d GlobalChangeLab

Create migration

    > ./manage.py schemamigration global_change_lab skills --initial

Execute migration

    > ./manage.py migrate global_change_lab skills NNNN

e.g. `NNNN = 0008`

### Further steps
Further steps should be done like this

Create migration

    > ./manage.py schemamigration global_change_lab skills
    Hubba hubba created migration NNNN

Edit migration (to e.g. add values to new fields)

    > vim global_change_lab/migration/NNNN_something.py

Execute migration

    > ./manage.py migrate global_change_lab skills NNNN

SASS/SCSS compilers
-------------------
As we use Foundation 5 having a SCSS compiler is a must the default SCSS
compiler is a Ruby Gem. There is a Python project called
[pyScss](https://github.com/Kronuz/pyScss), but unfortunately it doesn't work
with Foundation 5 yet:

* <https://github.com/Kronuz/pyScss/issues/259>

That means we have to use the Ruby Gem, which doesn't play well with
the cloudControl Python buildpack. (I believe can be made to work though)

Removing unused CSS
-------------------

* The Node (Javascript) library [uncss](https://github.com/giakki/uncss)
* The Python library [mincss](https://github.com/peterbe/mincss). Also check
  this [blog post](http://www.peterbe.com/plog/mincss)
* Or the online service <http://www.csstrashman.com>

Minifying CSS, packaging JS-files
---------------------------------
To build the final `.css`-file served on the site I have the following build
process:

1. Compile from SCSS to CSS (SASS)
2. Remove unused CSS (uncss)
3. Minify CSS

To automate this I use a build-tool. I considered the following options:

**django-pipeline** would be awesome because then the build process wouldn't depend on
`node` (Javascript). But it doesn't really support pipeling (executing the three
 steps above in sequence) and it doesn't work with paths containing spaces.

**gulp** is an `npm` package and is optimized for easy pipelining (no
intermediate files) but it didn't work with `uncss`.

**grunt** just worked.

Overridding admin and comments templates
----------------------------------------
The templates from app are loaded in the order specified in `INSTALLED_APPS`.
This means that if you put your custom admin templates in
`myapp/templates/admin`, `myapp` should be listed before `django.contrib.admin`
in `INSTALLED_APPS`.
Otherwise the default templates in `django.contrib.admin` will be found first
when searching for templates, and will be used instead of your custom templates.
