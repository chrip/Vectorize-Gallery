function showPreview() {
  var str = $("form").serialize();
  $("#preview").attr('src', '/py/img/vectorGraphic?' + str);
}

$(function() {
  var input = $( "input[name='highpass_filter']" );
  $("#highpass_filter").slider({
    change: showPreview,
    value: input.val(),
    min: 1,
    max: 100,
    step: 1,
		slide: function( event, ui ) {
			input.val( ui.value );
		}
  });
  $(":radio").click(showPreview);
  $("select").change(showPreview);
  //$("input").change(showPreview);
});
