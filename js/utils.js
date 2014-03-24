
var sendMessage = function(msg, class_attr, duration) {
  this.$messages = this.$messages || $('#messages');

  console.log('Send message', this.$messages);

  if (typeof(class_attr) === 'undefined') { class_attr = 'success'; }
  if (typeof(duration)   === 'undefined') { duration = 2000; }

  $message = $('<div class="alert-box ' + class_attr + '" data-alert>' + msg + '<a href="#" class="close">&times;</a></div>');
  $message.hide();

  $messages.append($message);

  $message.fadeIn(1000).delay(duration).fadeOut({
    duration: 1000,
    complete: function() { this.remove(); }
  });
};


$(document).ready(function() {

  // Make django message disappear after a while
  var $messages = $('#messages');
  $messages.children().each(function(i, el) {
    $(el).delay( (3 + i) * 1000).fadeOut({
      duration: 1000,
      complete: function() { this.remove(); }
    });
  });

  /*********** AJAX DELETION FUNCTIONS AND HANDLERS *************/
  var ajaxDelete = function($a) {
    console.log('AJAX getting:', $a.attr('href'));

    $.ajax({
      url: $a.attr('href'),

      error: function() {
        sendMessage('Object could not be deleted');
      },

      success: function() {
        // Unfortunately we need to use a class because the jQuery selector
        // syntax doesn't support `data-...` attributes
        $a.closest('.gcl-object').remove();
        sendMessage('Object was deleted');
      }
    });
  };

  // *** HARD DELETE ***
  // Add utility delete event handler that prompts the user to write "delete"
  // in order delete the object. All <a>'s with class="hard-delete ..." will get this
  // handler
  var classNameHardDelete = 'hard-delete';
  var hardDelete = function(e) {
    $a = $(this);

    var user_prompt = prompt('Please write "delete" to accept deleting this object');
    var error_msg = 'Object was not deleted, write <strong>delete</strong> to delete';

    if (user_prompt === 'delete') {
      // jQuery does type coercion on `data` attributes: string("false") -> bool(false)
      if ($a.data('dynamic') === false) {
        return true;
      } else {
        ajaxDelete($a);
      }
    } else {
      sendMessage(error_msg, 'alert');
    }
    e.preventDefault();
  };

  $(document).on('click', 'a.' + classNameHardDelete, function(e) {
    hardDelete.apply(this, [e]);
  });

  // *** SOFT DELETE ***
  // Add utility delete event handler that prompts the to click "Delete" or
  // "Cancel" in order delete the object.
  // All <a>'s with class="<classNameSoftDelete> ..." will get this handler
  var classNameSoftDelete = 'soft-delete';
  $(document).on('click', 'a.' + classNameSoftDelete, function(e) {
    e.preventDefault();

    var $a = $(this);
    var href = $a.attr('href');
    $a.data('dropdown', 'soft-delete-dropdown');
    var dropdown_id = $a.data('dropdown');

    var dropdown = '';
    dropdown +=   '<div class="f-dropdown delete-dropdown" id="' + dropdown_id + '" data-dropdown-content>';
    dropdown +=   '  <div>Really remove this comment?</div>';
    dropdown +=   '</div>';
    var $dropdown = $(dropdown);
    $dropdown.on('closed', function() { $dropdown.remove(); });

    var $delete_button = $('<a href="#" class="button">Delete</a>');
    $delete_button.click(function(e) {
      e.preventDefault();
      ajaxDelete($a);
      $dropdown.foundation('dropdown', 'close', $dropdown);
    });

    var $cancel_button = $('<a href="#" class="button close info">Cancel</a>');
    $cancel_button.click(function(e) {
      e.preventDefault();
      $dropdown.foundation('dropdown', 'close', $dropdown);
    });

    $dropdown.append($delete_button).append($cancel_button);
    $dropdown.appendTo($('body'));
    // $dropdown.foundation('dropdown', 'open', $dropdown);
    // $dropdown.foundation('dropdown', 'open', [$dropdown, $a]);

  });

  /************ INFO BOX ************/
  // don't show it if the user already closed it previously
  var $info_box = $('#info-box');
  var url_name = $info_box.data('url-name');
  var cookie = $.cookie('GCL.info_box_closed.' + url_name);
  if (cookie !== 'closed' && $info_box.children('.text').text() !== '') {
    $info_box.slideDown();
  }

  $info_box.children('a.close').click(function(e) {
    e.preventDefault();

    $.cookie('GCL.info_box_closed.' + url_name, 'closed');

    $info_box.fadeOut(1300);
  });


  /****************** PROJECTS *******************/
  // Resize embeds
  $('.project iframe').each(function() {
    var $this = $(this);
    var aspect_ratio = $this.width()/$this.height();
    var $project = $this.closest('.project');
    $this.width($project.width());
    $this.height($this.width() / aspect_ratio);
  });

  /****************** COMMENTS *******************/
  // AJAX submit comments
  $('form.comment-form').ajaxForm({
    resetForm: true,
    success: function(data, statusText, xhr, $form) {
      sendMessage('Comment successfully saved', 'success');
      var parent_pk = $form.find('input[name=parent]').val();
      if (parent_pk === '') {
        $form.closest('.comments').children('.comment-list').append(data['comment_html']);
      } else {
        var replies = $('<div class="replies" />');
        var $comment = $('#comment-' + parent_pk);

        if ($comment.next().hasClass('replies')) {
          replies = $comment.next();
        } else if ($comment.next().next().hasClass('replies')) {
          replies = $comment.next().next();
        } else {
          replies.after($comment);
        }
        replies.append(data['comment_html']);
      }
    },
    error: function(data, statusText, xhr, $form) {
      sendMessage('Comment could not be saved', 'error');
    }
  });

  // jQuery Autosize on comment fields
  // www.jacklmoore.com/autosize/
  $('textarea.comment').autosize();

  var $div = $('.comment-form').first();
  $('.replies').each(function() {
    var $this = $(this);
    var $new_div = $div.clone();
    var $reply_form = $new_div.children('form').first();
    // $reply_form.attr('action', $this.attr('href'));
    $reply_form.append('<input type="hidden" name="parent_pk" value="' + $this.data('parent-pk') + '">');
    $reply_form.children('input[name=project]').val($this.data('project-pk'));
    $new_div.appendTo($this);
    $new_div.hide();
  });

  // comment Reply button
  $('.comment a.reply').click(function(e) {
    e.preventDefault();

    var $a = $(this);
    var $comment = $a.closest('.comment');

    var $comments = $a.closest('.comments');
    if ($comments.data('comment_form_container') === undefined) {
      var $comment_form_container = $comments.children('.comment-form-container');
      $comments.data('comment_form_container', $comment_form_container);
    } else {
      var $comment_form_container = $comments.data('comment_form_container');
    }
    var $comment_form = $comment_form_container.children('.comment-form');

    // This reply link/form already active
    if ($a.hasClass('active')) {
      $comments.append($comment_form_container);
      $comment_form_container.removeClass('reply');

      $comment_form.find('input[name=parent]').val('');
      $a.removeClass('active');
      $a.text('Reply');

    } else {
      $comments.find('a.active').removeClass('active');
      $a.addClass('active');
      $a.text('Close');

      $comment_form.find('input[name=parent]').val($a.data('parent-pk'));

      $comment.after($comment_form_container);
      // inset to match visual style of replies
      $comment_form_container.addClass('reply');
    }

  });

  /************* LIKES ************/
  $('a.like, a.unlike').click(function(e) {
    e.preventDefault();

    var $a = $(this);
    var liking = true;
    if ($a.hasClass('unlike')) {
      liking = false;
    }

    $.ajax({
      type: 'POST',
      headers: { 'X-CSRFToken': $a.data('csrf_token') },
      data: {
        'content_type': $a.data('content_type'),
        'object_id': $a.data('object_id'),
        //'csrf_token':
      },
      url: $a.attr('href'),
      success: function() {
        if (liking) {
          //sendMessage('You liked something!', 'success');
          $a.removeClass('like');
          $a.addClass('unlike');
          $a.text('Unlike');

          $("#like-count div").animate({top: "-1.2rem"}, 400);
        } else {
          //sendMessage('You no longer like this', 'info');
          $a.removeClass('unlike');
          $a.addClass('like');
          $a.text('Like');

          $("#like-count div").animate({top: "0rem"}, 400);
        }
      },
      error: function(data) {
        if (liking) {
          sendMessage('Error in liking', 'error');
        } else {
          sendMessage('Could not unlike', 'error');
        }
      },
    });
  });

  /************* FILE (IMAGE) UPLOAD ************/
  $('.image-upload').each(function() {
    var $image_upload = $(this);

    var $fileupload = $image_upload.find('input[type=file]');
    var fileupload_url = $fileupload.data('url');
    var fileupload_uid = $fileupload.data('uid');
    var fileupload_csrf = $fileupload.data('csrf');

    var $dropzone = $image_upload.children('.dropzone');

    $fileupload.fileupload({
      url: fileupload_url,
      dataType: 'json',
      // Enable image resizing, except for Android and Opera,
      // which actually support image resizing, but fail to
      // send Blob objects via XHR requests:
      disableImageResize: /Android(?!.*Chrome)|Opera/
          .test(window.navigator && navigator.userAgent),

      imageMaxWidth: 200,
      imageMaxHeight: 200,

      formData: [
          { name: "uid", value: fileupload_uid},
          { name: "csrfmiddlewaretoken", value: fileupload_csrf}
      ],
      // {# maxFileSize: {{ maxfilesize }}, #}
      sequentialUploads: true,
      //imageCrop: true // Force cropped images

      dropZone: $dropzone,

      add: function (e, data) {
        $.each(data.files, function (index, file) {
          console.log('Selected file: ' + file.name);
        });
        data.submit();
        var progressbar = $('<div class="progress success round"> <span class="meter" style="width: 0%"></span> </div>');
        $dropzone.children('.helptext').html('');
        $dropzone.children('.helptext').append(progressbar);
      },
      progressall: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $dropzone.children('.helptext div.progress span.meter').css( 'width', progress + '%');
      },
      done: function (e, data) {
        console.log('Done uploading file: "' + data.result[0].url + '".');
        $dropzone.children('.helptext').html('');
        $dropzone.css('background-image', 'url(' + data.result[0].url + ')');
        // $('image-input-hidden').val(dropzone.css('background-image', 'url(' + data.result[0].url + ')');

        // {# $.each(data.result.files, function (index, file) { #}
        // {#   console.log('Done uploading.'); #}
        // {#   $('header').text(file.name); #}
        // {# }); #}

      }
      // {# change: function (e, data) { #}
      // {#   $.each(data.files, function (index, file) { #}
      // {#     alert('Selected file: ' + file.name); #}
      // {#   }); #}
      // {# }, #}

    }).prop('disabled', !$.support.fileInput)
      .parent().addClass($.support.fileInput ? undefined : 'disabled');

    // Add dropzone "hover while dragging" effect
    // {# https://github.com/blueimp/jQuery-File-Upload/wiki/Drop-zone-effects #}

    // dragenter
    $dropzone.on('mouseenter dragenter', null, null, function(e) {
      console.log('hovering');
      $(this).addClass('dragging-into');
    });
    // dragleave
    $dropzone.on('mouseleave dragleave', null, null, function(e) {
      console.log('unhovering');
      $(this).removeClass('dragging-into');
    });

  });



});
