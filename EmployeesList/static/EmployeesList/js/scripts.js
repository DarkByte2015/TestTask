$(document).on('click', '#is_working', function() {
  $(this).is(':checked') ? $('[is_working="false"').hide() : $('[is_working').show();
});

$(document).on('click', '.dep', function() {
  var id = $(this).attr('id');
  var sel = '[depid="' + id + '"]';
  $(this).is(':checked') ? $(sel).show() : $(sel).hide();
});
