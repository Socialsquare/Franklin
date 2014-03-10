
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
  // in order delete the object. All <a>'s with class="delete ..." will get this
  // handler
  var classNameHardDelete = 'delete';
  var hardDelete = function() {
    $a = $(this);

    var user_prompt = false;
    var error_msg = '';
    user_prompt = prompt('Please write "delete" to accept deleting this object') === 'delete';
    error_msg = 'Object was not deleted, write <strong>delete</strong> to delete';

    if (user_prompt) {
      ajaxDelete($a);
    } else {
      sendMessage(error_msg, 'alert');
    }
  };

  $('body #content').on('click', 'a.' + classNameHardDelete, function(e) {
    // call with `hard_delete = true`
    hardDelete.apply(this, []);
    e.preventDefault();
  });

  // *** SOFT DELETE ***
  // Add utility delete event handler that prompts the to click "Delete" or
  // "Cancel" in order delete the object.
  // All <a>'s with class="<classNameSoftDelete> ..." will get this handler
  var classNameSoftDelete = 'soft-delete';
  $('body #content').on('click', 'a.' + classNameSoftDelete, function(e) {
    e.preventDefault();

    var $a = $(this);
    var href = $a.attr('href');
    $a.data('dropdown', 'soft-delete-dropdown');
    var dropdown_id = $a.data('dropdown');

    var dropdown = '';
    dropdown +=   '<div id="' + dropdown_id + '" class="f-dropdown" data-dropdown-content>';
    dropdown +=   '  <h6>Really remove this comment?</h6>';
    dropdown +=   '</div>';
    var $dropdown = $(dropdown);
    $dropdown.on('closed', function() { $dropdown.remove(); });

    var $delete_button = $('<a href="#" class="button">Delete</a>');
    $delete_button.click(function() {
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

  $('.project div.content').each(function() {
    var $this = $(this);
    var $p = $this.children('p');
    console.log($p.css('height'), $this.css('max-height'));
    if ($p.height() < $this.height()) {
      $this.children('.gradient').hide();
      $this.closest('.project').children('.expand').hide();
    }
  });

  $('.project a.expand').click(function(e) {
    e.preventDefault();
    var $project = $(this).closest('.project');
    var $project_content = $project.children('.content');
    var $gradient = $project_content.children('.gradient');

    $project_content.data('previous-max-height', $project_content.css('max-height'));
    $project_content.css('max-height', 'none');
    $gradient.hide();

    $(this).remove();
  });
  $('.project a.collapse').click(function(e) {
    e.preventDefault();
    var $project_content = $(this).parent().parent();
    var $shower = $project_content.children('.shower');
    var $hider = $project_content.children('.hider');

    $project_content.css('max-height', $project_content.data('previous-max-height'));
    $hider.hide();
    $shower.show();
  });

  // Resize embeds
  $('.project iframe').each(function() {
    var $this = $(this);
    var aspect_ratio = $this.width()/$this.height();
    var $project = $this.closest('.project');
    $this.width($project.width());
    $this.height($this.width() / aspect_ratio);
  });

  /****************** COMMENTS *******************/

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

  $('.comment a.reply').click(function(e) {
    e.preventDefault();

    var $a = $(this);
    var $comment = $a.closest('.comment');

    var $div = $('.comment-form').first().clone();


    console.log('clicked reply');
    $comment.append($div);

  });

});
