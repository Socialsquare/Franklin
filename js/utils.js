
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
  // $('a.delete').click(function(e) {
  $('body #content').on('click', 'a.delete', function(e) {
    e.preventDefault();
    $a = $(this);

    console.log('deleting...');

    if (prompt('Please write "delete" to accept deleting this object') === 'delete') {
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

    } else {
      sendMessage('Object was not deleted, write <strong>delete</strong> to delete', 'alert');
    }
  });
});
