/*global $:false, d3:false, nv:false, get_shot_type_pie_chart:false, data:false */

function pie_chart(data, selector) {
    console.log(data);
  return nv.addGraph(function () {

      // First we clean any previous drawing (We call the function again
      // when the window is re-sized).

      d3.select(selector).selectAll('g').remove();


    var width = $(selector).width(),
      height = width;

    var chart = nv.models.pieChart()
        .x(function (d) { return d.key; })
        .y(function (d) { return d.y; })
        .color(d3.scale.category10().range())
        .width(width)
        .height(height);

    d3.select(selector)
        .datum(data)
      .transition().duration(1200)
        .attr('width', width)
        .attr('height', height)
        .call(chart);

    chart.dispatch.on('stateChange', function (e) { nv.log('New State:', JSON.stringify(e)); });

    return chart;
  });
}


function pie_chart_shot_type (shot_list) {
//    if (error) {
//        return console.warn(error);
//    }
    var shot_type_pie_chart = get_shot_type_pie_chart(shot_list);
    pie_chart(shot_type_pie_chart, "#test1");
}


//$(document).ready(function() {
//    var data_shots = get_data_shots(data.points);
//    pie_chart_shot_type(error, data_shots);
//  });



