if (window.console === undefined) {
    window.console = {
        log: function(string) {},
        err: function(string) {}
    };
}


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
  // Nothing here


  /****************** COMMENTS *******************/

  // jQuery Autosize on comment fields
  // www.jacklmoore.com/autosize/
  $('textarea.comment').autosize();


  // AJAX submit comments
  var ajax_form_settings = {
    resetForm: true,
    success: function(data, statusText, xhr, $form) {
      sendMessage('Comment successfully saved', 'success');
      var parent_pk = $form.find('input[name=parent]').val();
      var $comment = $(data['comment_html']);
      $comment.hide();

      if (parent_pk === '') {
        $('.comment-list .missing-message').remove();

        $('.comment-list').prepend($comment);
        $comment.fadeIn();
      } else {
        // var $replies = $form.closest('.replies');
        // $replies.prepend($comment);
        $form.after($comment);
        $comment.fadeIn();
      }
    },
    error: function(data, statusText, xhr, $form) {
      sendMessage('Comment could not be saved', 'error');
    }
  };

  $('form.comment-form').ajaxForm(ajax_form_settings);

  // Flag and delete buttons
  //   I know - sorry - this is overly complex, but I just don't want to have
  //   two times the code for these event handlers lying around (DRY)
  var actions = {
    'delete': function($a) {
      $a.closest('.comment').slideUp();
      var comment_pk = $a.closest('.comment').data('comment-pk');
      $('#replies-for-' + comment_pk).slideUp();
    },
    'flag':   function($a) { $a.text('Flagged'); },
    'unflag':   function($a) { $a.text('Unflagged'); }
  };
  for (var action in actions) {

    // Create event handlers
    //   ... avoiding Javascript variable capture, ugh...
    //   also, the fact that `$(this)` actually ends up referring to the <a> is
    //   kind of lucky.
    var func = (function(action) {
      return function(e) {
        var $a = $(this);

        // Change text to match "Flag comment"/"Flag share"
        var object_type = $a.data('object-type');
        var $dropdown = $('#' + action + '-dropdown').find('.object-type').text(object_type);

        // Close dropdown event handler
        $('#' + action + '-dropdown a.close').click(function(e) {
          e.preventDefault();
          $(document).foundation('dropdown', 'close', $('#' + $a.data('dropdown')));
        });

        // Confirm action event handler
        $('#' + action + '-dropdown a.' + action).click(function(e) {
          e.preventDefault();
          $a.css('visibility', 'visible');

          $.ajax({
            type: 'GET',
            url: $a.attr('href'),
            success: function() {
              actions[action]($a);
              $(document).foundation('dropdown', 'close', $('#' + $a.data('dropdown')));
            },
            error: function(data) {
              sendMessage('Error: Could not ' + action, 'error');
            }
          });
        });
      };
    })(action);

    // Bind event handlers
    $('.comment a.' + action).click(func);
    $('a.' + action).click(func);
  }

  // Reply button
  $('.comment a.reply').click(function(e) {
    e.preventDefault();

    var $a = $(this);

    var $comment = $a.closest('.comment');
    var comment_pk = $comment.data('comment-pk');
    var $replies = $('#replies-for-' + comment_pk);

    // This reply link/form already active
    if ($a.hasClass('active')) {
      // Remove the reply form
      $a.data('reply-form').remove();

      // Change the link text
      $a.removeClass('active');
      $a.text('Reply');
    } else {
      // Add the reply form
      var $reply_form = $('form.reply-form').first().clone();
      $reply_form.ajaxForm(ajax_form_settings);

      $a.data('reply-form', $reply_form);
      $replies.prepend($reply_form);
      $reply_form.show();

      // Set the parent primary key (the ID)
      $reply_form.find('input[name=parent]').val($a.data('parent-pk'));

      // Change the link text
      $a.addClass('active');
      $a.text('Close');
    }

  });

  /************* LIKES ************/
  $('a.like, a.unlike').click(function(e) {

    var $a = $(this);
    if ($a.data('object_id')) {
      e.preventDefault();
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

            $("#like-count div").animate({top: "-1em"}, 400);
          } else {
            //sendMessage('You no longer like this', 'info');
            $a.removeClass('unlike');
            $a.addClass('like');
            $a.text('Like');

            $("#like-count div").animate({top: "0em"}, 400);
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
    }
  });

  /************* TOOLTIPS ************/
  $('.tooltip').each(function(el) {
    var $el = $(this);
    if ($el.data('tooltip') !== undefined) {
      $el.poshytip({
        className: 'tip-twitter',
        alignTo: 'target',
        alignX: 'center',
        alignY: 'bottom',
        content: $el.data('tooltip')
      });
    }
  });

  /************* FILE (IMAGE) UPLOAD ************/
  $('.image-upload').each(function() {
    var $image_upload = $(this);

    var $fileupload = $image_upload.find('input[type=file]');
    var fileupload_url = $fileupload.data('url');
    var fileupload_uid = $fileupload.data('uid');
    var fileupload_csrf = $fileupload.data('csrf');
    var fileupload_identifier = $fileupload.data('identifier');

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
          { name: "csrfmiddlewaretoken", value: fileupload_csrf},
          { name: "identifier", value: fileupload_identifier}
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
        $dropzone.children('.helptext div.progress span.meter').css('width', progress + '%');
      },
      done: function (e, data) {
        console.log('Done uploading file: "' + data.result[0].url + '".');
        $dropzone.children('.helptext').html('');
        $dropzone.css('background-image', 'url(' + data.result[0].url + ')');
        $image_upload.data('image_url', data.result[0].url);
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
