Frontend
========

Javascript management
---------------------
I don't want to include Javascript dependencies like jQuery and Backbone in the
git repository, but I need to specify where the files are and what libraries I'm
using.

There exists a plethora of package manager that do exactly this

* ender
* volo
* jam
* webpack
* webmake
* component (uses its own packages: <http://component.io>)
* bower (uses Github)

CommonJS vs AMD
Browserify vs RequireJS (r.js)
also curl.js

This discussion never ends and is just a huge timesuck.

I like the clear-cut modules and imports of RequireJS, but it doesn't allow me
to write inline Javascript in my HTML.

I'm just gonna minify the my Javascript dependencies into two bundles
`user.min.js` and `trainer.min.js`.

<http://procbits.com/2013/06/17/client-side-javascript-management-browserify-vs-component>
<http://www.reddit.com/r/javascript/comments/vc9d9/npm_vs_jam_requirejs_vs_browserify_vs_ender/>
<https://github.com/yeoman/yeoman/wiki/Front-end-package-management-with-Bower#wiki-what-distinguishes-bower-from-jam-volo-or-ender-what-does-it-do-better>

Uploads with progress bar
-------------------------
There are hundreds of those dynamic upload scripts. Most of them cost money.
<http://stackoverflow.com/questions/4162102/html-5-file-upload>
<https://developer.mozilla.org/en-US/docs/Using_files_from_web_applications>

**Free**
* [jQuery File Upload Plugin](https://github.com/blueimp/jQuery-File-Upload)
  Nice, large Github project.
  This is the one we're using.
  For more info check out <https://github.com/blueimp/jQuery-File-Upload/wiki>.
* <http://html5demos.com/dnd-upload#view-source>
* [DropzoneJS](http://www.dropzonejs.com)
* [jQuery Filedrop]https://github.com/weixiyen/jquery-filedrop/)
* [html5uploader](http://code.google.com/p/html5uploader/)
* [Plupload](http://www.plupload.com/)
  GPLv2 licensed, pay to get other license
* <http://www.matlus.com/html5-file-upload-with-progress/>
* [jQuery Fileuploader Plugin](http://pixelcone.com/fileuploader/)
  Ugly homepage
* [List of 12](http://designscrazed.com/html5-jquery-file-upload-scripts/)

**Paid**

* [Pure Uploader](http://codecanyon.net/item/pure-uploader/4452882?ref=hdalive&ref=hdalive&clickthrough_id=201877193&redirect_back=true)


### Handling it with django

* <http://amatellanes.wordpress.com/2013/11/05/dropzonejs-django-how-to-build-a-file-upload-form/>
* <https://github.com/ouhouhsami/django-progressbarupload>

* <https://github.com/GoodCloud/django-ajax-uploader>
* <https://github.com/maraujop/django-crispy-forms>



Sticky footer
-------------
In order to get the footer be at the bottom of the window when content is short
you have to use a "sticky footer". The fix is as ugly as vertically centering
something...


Semantic HTML solution, fixed footer heigth:
<http://mystrd.at/modern-clean-css-sticky-footer/>


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
And by-the-way lists and headings
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


https://github.com/yeoman/yeoman/wiki/Front-end-package-management-with-Bower

Backend
=======

Forgot admin password?
----------------------
Here's a way to reset it:

    $ ./manage.py shell
    Python 3.3.3 (default, Nov 26 2013, 13:33:18)
    [GCC 4.8.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> from global_change_lab.models import User
    >>> User.objects.filter(username='malthe')
    [<User: malthe>]
    >>> m = User.objects.filter(username='malthe')[0]
    >>> m.set_password('kodeord')
    >>> m.save()


Sorting
-------

* [django-sortable](https://github.com/drewyeaton/django-sortable)
* [django-sorter](http://django-sorter.readthedocs.org/en/latest/)

Permissions management
----------------------
According to <http://djangopackages.com> there are 3 permission-management
packages compatible with Python 3:

* django-authority
* django-permission
* django-permissionx

### django-permission
The documentation is lacking, and it doesn't seem as well-though-out as
`django-authority` (caching, documentation).

But it works.
(Grab it from Github - not PyPi, the version on PyPi is old and doesn't work as
the readthedocs documentation specifies)

### django-authority
The examples are for django 1.0 and 1.1 - WTF.
The interface is nice and I think I got it to work for a minute or two. But in
the end it just kept on refusing to work.

**side note**:
After having added `authority` to `INSTALLED_APPS` I got the following error

    > python manage.py runserver

    Traceback (most recent call last):
      File "<OMITTED>/lib/python3.3/site-packages/django/core/urlresolvers.py", line 339, in urlconf_module
        return self._urlconf_module
    AttributeError: 'RegexURLResolver' object has no attribute '_urlconf_module'

### django-permissionx
Didn't like it. But maybe it deserves a revisit.


Email service
-------------
The first thing is that I don't want to send emails myself. Sending emails is
 ridiculously hard. [Jeff Atwood/codinghorror on email](http://www.codinghorror.com/blog/2010/04/so-youd-like-to-send-some-email-through-code.html)
I have been burned, hard, before so I'm not gonna send emails myself.
Luckily there are loads of services that offer sending emails for you.
Amazon Web Services have SES (Simple Email Service). But `django-ses` which is
the django module for using SES doesn't work with Python 3 _and_ it depends on
`boto` which also doesn't work Python 3.

`SendGrid`, which I'm using right now, just works.
<http://sendgrid.com/docs/Integrate/Frameworks/django.html>


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

Overridding admin and comments templates
----------------------------------------
The templates from app are loaded in the order specified in `INSTALLED_APPS`.
This means that if you put your custom admin templates in
`myapp/templates/admin`, `myapp` should be listed before `django.contrib.admin`
in `INSTALLED_APPS`.
Otherwise the default templates in `django.contrib.admin` will be found first
when searching for templates, and will be used instead of your custom templates.


Irrelevant news
===============

GIMP fails to save .png
-----------------------
I cut out some of the (skill) icons and stencil from the design. But it wouldn't
save the images as .png.  This is because of a new version of `libpng` and its
default color profile.
You can change that in GIMP under `Image > Mode > Assign color profile`.

Reference: <https://wiki.archlinux.org/index.php/Libpng_errors>
