function translate(x, y) {
    return 'translate(' + x + ',' + y + ')';
}

// canvas dimensions
var width = 400,
    height = 300,
    pad = 10;

var objectives = d3.select('#objectives').append('svg')
    .style('width', width + pad * 2)
    .style('height', height + pad * 2);

var x = d3.scale.linear()
    .domain([0, cw]) // width of a court
    .range([0, width]);

var y = d3.scale.linear()
    .domain([0, ch])
    .range([0, height]);


// baselines
objectives.selectAll('text')
    .data([50, 100, 150])
  .enter().append('text')
    .attr('x', 100)
    .attr('y', function(d){return d;})
    .attr('style', 'font-size: 25; font-family: sans-serif')
    .attr('fill', 'gray')
    .text('Distance parcourue');