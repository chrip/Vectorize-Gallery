function showPreview() {
  var str = $("form").serialize();
  $("#preview").attr('src', '/py/img/vectorGraphic?' + str);
}

$(function() {

  $(":radio").click(showPreview);
  $("select").change(showPreview);
  $("input").change(showPreview);
});
