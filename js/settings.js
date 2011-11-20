function showPreview() {
  var str = $("form").serialize();
  $("#preview").attr('src', '/py/img/vectorGraphic?' + str);
}

$(function() {
  $(":radio").click(showPreview);
  $("select").change(showPreview);
  
  // highpass_filter
  var hp = $( "input[name='highpass_filter']" );
  $("#highpass_filter_slider").slider({
    change: showPreview,
    value: hp.val(),
    min: 1,
    max: 100,
    step: 1,
		slide: function( event, ui ) {
			hp.val( ui.value );
		}
  });

  // scale_factor
  var sf = $( "input[name='scale_factor']" );
  $("#scale_factor_slider").slider({
    change: showPreview,
    value: sf.val(),
    min: 1,
    max: 8,
    step: 1,
		slide: function( event, ui ) {
			sf.val( ui.value );
		}
  });

  // threshold
  var th = $( "input[name='threshold']" );
  $("#threshold_slider").slider({
    change: showPreview,
    value: th.val(),
    min: 0,
    max: 1,
    step: 0.01,
		slide: function( event, ui ) {
			th.val( ui.value );
		}
  });

  // turdsize
  var ts = $( "input[name='turdsize']" );
  $("#turdsize_slider").slider({
    change: showPreview,
    value: ts.val(),
    min: 1,
    max: 1000,
    step: 1,
		slide: function( event, ui ) {
			ts.val( ui.value );
		}
  });

  // alphamax
  var am = $( "input[name='alphamax']" );
  $("#alphamax_slider").slider({
    change: showPreview,
    value: am.val(),
    min: -0.1,
    max: 1.334,
    step: 0.01,
		slide: function( event, ui ) {
			am.val( ui.value );
		}
  });

  // foreground_color
  function hexFromRGB(r, g, b) {
		var hex = [
			r.toString( 16 ),
			g.toString( 16 ),
			b.toString( 16 )
		];
		$.each( hex, function( nr, val ) {
			if ( val.length === 1 ) {
				hex[ nr ] = "0" + val;
			}
		});
		return hex.join( "" ).toUpperCase();
	}
  var fc = $( "input[name='foreground_color']" );
	function refreshInput() {
		var red = $( "#red" ).slider( "value" ),
			green = $( "#green" ).slider( "value" ),
			blue = $( "#blue" ).slider( "value" ),
			hex = hexFromRGB( red, green, blue );
		  fc.val( hex );
	}
	$(function() {
		$( "#red, #green, #blue" ).slider({
      change: showPreview,
			range: "min",
      min:0,
			max: 255,
      step: 1,
			value: 0,
			slide: refreshInput
		});
		$( "#red" ).slider( "value", parseInt(fc.val().substring(0,2),16) );
		$( "#green" ).slider( "value", parseInt(fc.val().substring(2,4),16) );
		$( "#blue" ).slider( "value", parseInt(fc.val().substring(4,6),16) );
	});
});
