
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


  // Add utility delete event handler that prompts the user to write "delete"
  // in order delete the object. All <a>'s with class="delete ..." will get this
  // handler
  $('body #content').on('click', 'a.delete', function(e) {
    $a = $(this);

    console.log('deleting...');
    console.log($a.data('dynamic'));

    if (prompt('Please write "delete" to accept deleting this object') === 'delete') {

      console.log($a.data('dynamic'));
      if ($a.data('dynamic') === false) {
        return true;
      } else {
        console.log('AJAX getting:', $a.attr('href'));
        e.preventDefault();

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
      }

    } else {
      sendMessage('Object was not deleted, write <strong>delete</strong> to delete', 'alert');
    }
    e.preventDefault();
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
      $this.children('.shower').hide();
    }
  });

  $('.project a.expand').click(function(e) {
    e.preventDefault();
    var $project_content = $(this).parent().parent();
    var $shower = $project_content.children('.shower');
    var $hider = $project_content.children('.hider');

    $project_content.data('previous-max-height', $project_content.css('max-height'));
    $project_content.css('max-height', 'none');
    $shower.hide();
    $hider.show();
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
