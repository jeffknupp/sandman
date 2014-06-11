/*
 * GRAPH ELEMENT NAMES
 *
 * #sales-graph 
 * #area-graph
 * #bar-graph
 * #normal-bar-graph
 * #noline-bar-graph
 * #year-graph
 * #decimal-graph
 * #donut-graph
 * #time-graph
 * #graph-B
 * #nogrid-graph
 * #non-continu-graph
 * #non-date-graph
 * #stacked-bar-graph
 * #interval-graph - animated graph
 */ 
 
 
$(document).ready( function() {    
	if ($('#sales-graph').length){ 
		
	 Morris.Area({
	    element: 'sales-graph',
	    data: [
	      {period: '2010 Q1', iphone: 2666, ipad: null, itouch: 2647},
	      {period: '2010 Q2', iphone: 2778, ipad: 2294, itouch: 2441},
	      {period: '2010 Q3', iphone: 4912, ipad: 1969, itouch: 2501},
	      {period: '2010 Q4', iphone: 3767, ipad: 3597, itouch: 5689},
	      {period: '2011 Q1', iphone: 6810, ipad: 1914, itouch: 2293},
	      {period: '2011 Q2', iphone: 5670, ipad: 4293, itouch: 1881},
	      {period: '2011 Q3', iphone: 4820, ipad: 3795, itouch: 1588},
	      {period: '2011 Q4', iphone: 15073, ipad: 5967, itouch: 5175},
	      {period: '2012 Q1', iphone: 10687, ipad: 4460, itouch: 2028},
	      {period: '2012 Q2', iphone: 8432, ipad: 5713, itouch: 1791}
	    ],
	    xkey: 'period',
	    ykeys: ['iphone', 'ipad', 'itouch'],
	    labels: ['iPhone', 'iPad', 'iPod Touch'],
	    pointSize: 2,
	    hideHover: 'auto'
	  });
	  
	}
	
	// area graph
	if ($('#area-graph').length){ 
		Morris.Area({
		  element: 'area-graph',
		  data: [
		    {x: '2011 Q1', y: 3, z: 3},
		    {x: '2011 Q2', y: 2, z: 0},
		    {x: '2011 Q3', y: 0, z: 2},
		    {x: '2011 Q4', y: 4, z: 4}
		  ],
		  xkey: 'x',
		  ykeys: ['y', 'z'],
		  labels: ['Y', 'Z']
		});
	}
	
	// bar graph color
	if ($('#bar-graph').length){ 
		
		Morris.Bar({
		  element: 'bar-graph',
		  data: [
		    {x: '2011 Q1', y: 0},
		    {x: '2011 Q2', y: 1},
		    {x: '2011 Q3', y: 2},
		    {x: '2011 Q4', y: 3},
		    {x: '2012 Q1', y: 4},
		    {x: '2012 Q2', y: 5},
		    {x: '2012 Q3', y: 6},
		    {x: '2012 Q4', y: 7},
		    {x: '2013 Q1', y: 8}
		  ],
		  xkey: 'x',
		  ykeys: ['y'],
		  labels: ['Y'],
		  barColors: function (row, series, type) {
		    if (type === 'bar') {
		      var red = Math.ceil(255 * row.y / this.ymax);
		      return 'rgb(' + red + ',0,0)';
		    }
		    else {
		      return '#000';
		    }
		  }
		});
	
	}
	
	
	
	// Use Morris.Bar
	if ($('#normal-bar-graph').length){ 
		
		Morris.Bar({
		  element: 'normal-bar-graph',
		  data: [
		    {x: '2011 Q1', y: 3, z: 2, a: 3},
		    {x: '2011 Q2', y: 2, z: null, a: 1},
		    {x: '2011 Q3', y: 0, z: 2, a: 4},
		    {x: '2011 Q4', y: 2, z: 4, a: 3}
		  ],
		  xkey: 'x',
		  ykeys: ['y', 'z', 'a'],
		  labels: ['Y', 'Z', 'A']
		});
	
	}
	
	
	// Use Morris.Bar 2
	if ($('#noline-bar-graph').length){ 
		Morris.Bar({
		  element: 'noline-bar-graph',
		  axes: false,
		  data: [
		    {x: '2011 Q1', y: 3, z: 2, a: 3},
		    {x: '2011 Q2', y: 2, z: null, a: 1},
		    {x: '2011 Q3', y: 0, z: 2, a: 4},
		    {x: '2011 Q4', y: 2, z: 4, a: 3}
		  ],
		  xkey: 'x',
		  ykeys: ['y', 'z', 'a'],
		  labels: ['Y', 'Z', 'A']
		});
	}
	
	/* data stolen from http://howmanyleft.co.uk/vehicle/jaguar_'e'_type */
	if ($('#year-graph').length){ 
		var day_data = [
		  {"period": "2012-10-01", "licensed": 3407, "sorned": 660},
		  {"period": "2012-09-30", "licensed": 3351, "sorned": 629},
		  {"period": "2012-09-29", "licensed": 3269, "sorned": 618},
		  {"period": "2012-09-20", "licensed": 3246, "sorned": 661},
		  {"period": "2012-09-19", "licensed": 3257, "sorned": 667},
		  {"period": "2012-09-18", "licensed": 3248, "sorned": 627},
		  {"period": "2012-09-17", "licensed": 3171, "sorned": 660},
		  {"period": "2012-09-16", "licensed": 3171, "sorned": 676},
		  {"period": "2012-09-15", "licensed": 3201, "sorned": 656},
		  {"period": "2012-09-10", "licensed": 3215, "sorned": 622}
		];
		Morris.Line({
		  element: 'year-graph',
		  data: day_data,
		  xkey: 'period',
		  ykeys: ['licensed', 'sorned'],
		  labels: ['Licensed', 'SORN']
		})
	}
	
	
	// decimal data
	if ($('#decimal-graph').length){ 
		var decimal_data = [];
		for (var x = 0; x <= 360; x += 10) {
		  decimal_data.push({
		    x: x,
		    y: Math.sin(Math.PI * x / 180).toFixed(4)
		  });
		}
		window.m = Morris.Line({
		  element: 'decimal-graph',
		  data: decimal_data,
		  xkey: 'x',
		  ykeys: ['y'],
		  labels: ['sin(x)'],
		  parseTime: false,
		  hoverCallback: function (index, options) {
		    var row = options.data[index];
		    return "sin(" + row.x + ") = " + row.y;
		  },
		  xLabelMargin: 10
		});
	}
	
	
	// donut
	if ($('#donut-graph').length){ 
		Morris.Donut({
		  element: 'donut-graph',
		  data: [
		    {value: 70, label: 'foo'},
		    {value: 15, label: 'bar'},
		    {value: 10, label: 'baz'},
		    {value: 5, label: 'A really really long label'}
		  ],
		  formatter: function (x) { return x + "%"}
		});
	}
	
	// time formatter
	if ($('#time-graph').length){ 
		var week_data = [
		  {"period": "2011 W27", "licensed": 3407, "sorned": 660},
		  {"period": "2011 W26", "licensed": 3351, "sorned": 629},
		  {"period": "2011 W25", "licensed": 3269, "sorned": 618},
		  {"period": "2011 W24", "licensed": 3246, "sorned": 661},
		  {"period": "2011 W23", "licensed": 3257, "sorned": 667},
		  {"period": "2011 W22", "licensed": 3248, "sorned": 627},
		  {"period": "2011 W21", "licensed": 3171, "sorned": 660},
		  {"period": "2011 W20", "licensed": 3171, "sorned": 676},
		  {"period": "2011 W19", "licensed": 3201, "sorned": 656},
		  {"period": "2011 W18", "licensed": 3215, "sorned": 622},
		  {"period": "2011 W17", "licensed": 3148, "sorned": 632},
		  {"period": "2011 W16", "licensed": 3155, "sorned": 681},
		  {"period": "2011 W15", "licensed": 3190, "sorned": 667},
		  {"period": "2011 W14", "licensed": 3226, "sorned": 620},
		  {"period": "2011 W13", "licensed": 3245, "sorned": null},
		  {"period": "2011 W12", "licensed": 3289, "sorned": null},
		  {"period": "2011 W11", "licensed": 3263, "sorned": null},
		  {"period": "2011 W10", "licensed": 3189, "sorned": null},
		  {"period": "2011 W09", "licensed": 3079, "sorned": null},
		  {"period": "2011 W08", "licensed": 3085, "sorned": null},
		  {"period": "2011 W07", "licensed": 3055, "sorned": null},
		  {"period": "2011 W06", "licensed": 3063, "sorned": null},
		  {"period": "2011 W05", "licensed": 2943, "sorned": null},
		  {"period": "2011 W04", "licensed": 2806, "sorned": null},
		  {"period": "2011 W03", "licensed": 2674, "sorned": null},
		  {"period": "2011 W02", "licensed": 1702, "sorned": null},
		  {"period": "2011 W01", "licensed": 1732, "sorned": null}
		];
		Morris.Line({
		  element: 'time-graph',
		  data: week_data,
		  xkey: 'period',
		  ykeys: ['licensed', 'sorned'],
		  labels: ['Licensed', 'SORN'],
		  events: [
		    '2011-04',
		    '2011-08'
		  ]
		});
	}
	
	// negative value
	if ($('#graph-B').length){ 
		var neg_data = [
		  {"period": "2011-08-12", "a": 100},
		  {"period": "2011-03-03", "a": 75},
		  {"period": "2010-08-08", "a": 50},
		  {"period": "2010-05-10", "a": 25},
		  {"period": "2010-03-14", "a": 0},
		  {"period": "2010-01-10", "a": -25},
		  {"period": "2009-12-10", "a": -50},
		  {"period": "2009-10-07", "a": -75},
		  {"period": "2009-09-25", "a": -100}
		];
		Morris.Line({
		  element: 'graph-B',
		  data: neg_data,
		  xkey: 'period',
		  ykeys: ['a'],
		  labels: ['Series A'],
		  units: '%'
		});
	}
	
	// no grid
	/* data stolen from http://howmanyleft.co.uk/vehicle/jaguar_'e'_type */
	if ($('#nogrid-graph').length){ 
		var day_data = [
		  {"period": "2012-10-01", "licensed": 3407, "sorned": 660},
		  {"period": "2012-09-30", "licensed": 3351, "sorned": 629},
		  {"period": "2012-09-29", "licensed": 3269, "sorned": 618},
		  {"period": "2012-09-20", "licensed": 3246, "sorned": 661},
		  {"period": "2012-09-19", "licensed": 3257, "sorned": 667},
		  {"period": "2012-09-18", "licensed": 3248, "sorned": 627},
		  {"period": "2012-09-17", "licensed": 3171, "sorned": 660},
		  {"period": "2012-09-16", "licensed": 3171, "sorned": 676},
		  {"period": "2012-09-15", "licensed": 3201, "sorned": 656},
		  {"period": "2012-09-10", "licensed": 3215, "sorned": 622}
		];
		Morris.Line({
		  element: 'nogrid-graph',
		  grid: false,
		  data: day_data,
		  xkey: 'period',
		  ykeys: ['licensed', 'sorned'],
		  labels: ['Licensed', 'SORN']
		});
	}
	
	// non-continus data
	/* data stolen from http://howmanyleft.co.uk/vehicle/jaguar_'e'_type */
	if ($('#non-continu-graph').length){ 
		var day_data = [
		  {"period": "2012-10-01", "licensed": 3407},
		  {"period": "2012-09-30", "sorned": 0},
		  {"period": "2012-09-29", "sorned": 618},
		  {"period": "2012-09-20", "licensed": 3246, "sorned": 661},
		  {"period": "2012-09-19", "licensed": 3257, "sorned": null},
		  {"period": "2012-09-18", "licensed": 3248, "other": 1000},
		  {"period": "2012-09-17", "sorned": 0},
		  {"period": "2012-09-16", "sorned": 0},
		  {"period": "2012-09-15", "licensed": 3201, "sorned": 656},
		  {"period": "2012-09-10", "licensed": 3215}
		];
		Morris.Line({
		  element: 'non-continu-graph',
		  data: day_data,
		  xkey: 'period',
		  ykeys: ['licensed', 'sorned', 'other'],
		  labels: ['Licensed', 'SORN', 'Other'],
		  /* custom label formatting with `xLabelFormat` */
		  xLabelFormat: function(d) { return (d.getMonth()+1)+'/'+d.getDate()+'/'+d.getFullYear(); },
		  /* setting `xLabels` is recommended when using xLabelFormat */
		  xLabels: 'day'
		});
	}
	
	// non date data
	if ($('#non-date-graph').length){ 
		var day_data = [
		  {"elapsed": "I", "value": 34},
		  {"elapsed": "II", "value": 24},
		  {"elapsed": "III", "value": 3},
		  {"elapsed": "IV", "value": 12},
		  {"elapsed": "V", "value": 13},
		  {"elapsed": "VI", "value": 22},
		  {"elapsed": "VII", "value": 5},
		  {"elapsed": "VIII", "value": 26},
		  {"elapsed": "IX", "value": 12},
		  {"elapsed": "X", "value": 19}
		];
		Morris.Line({
		  element: 'non-date-graph',
		  data: day_data,
		  xkey: 'elapsed',
		  ykeys: ['value'],
		  labels: ['value'],
		  parseTime: false
		});
	}
	
	//stacked bar
	if ($('#stacked-bar-graph').length){ 
		Morris.Bar({
		  element: 'stacked-bar-graph',
		  axes: false,
		  grid: false,
		  data: [
		    {x: '2011 Q1', y: 3, z: 2, a: 3},
		    {x: '2011 Q2', y: 2, z: null, a: 1},
		    {x: '2011 Q3', y: 0, z: 2, a: 4},
		    {x: '2011 Q4', y: 2, z: 4, a: 3}
		  ],
		  xkey: 'x',
		  ykeys: ['y', 'z', 'a'],
		  labels: ['Y', 'Z', 'A'],
		  stacked: true
		});
	}
	
	// interval 
	
	if ($('#interval-graph').length){ 
		
		var nReloads = 0;
		function data(offset) {
		  var ret = [];
		  for (var x = 0; x <= 360; x += 10) {
		    var v = (offset + x) % 360;
		    ret.push({
		      x: x,
		      y: Math.sin(Math.PI * v / 180).toFixed(4),
		      z: Math.cos(Math.PI * v / 180).toFixed(4)
		    });
		  }
		  return ret;
		}
		var graph = Morris.Line({
		    element: 'interval-graph',
		    data: data(0),
		    xkey: 'x',
		    ykeys: ['y', 'z'],
		    labels: ['sin()', 'cos()'],
		    parseTime: false,
		    ymin: -1.0,
		    ymax: 1.0,
		    hideHover: true
		});
		function update() {
		  nReloads++;
		  graph.setData(data(5 * nReloads));
		  $('#reloadStatus').text(nReloads + ' reloads');
		}
		setInterval(update, 100);
	}
}); 	
