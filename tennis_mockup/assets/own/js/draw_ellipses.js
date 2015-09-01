/*global $:false, d3:false */

function draw_ellipses(selector, data_shots, attribute_to_draw){
    var court_data = define_court_data();

    var width = court_data.width,
        height = court_data.height,
        padx = court_data.padx,
        pady = court_data.pady;

    var scale_point_x = d3.scale.linear()
                            .domain([0, 1])
                            .range([0, width + padx*2]);

    var scale_point_y = d3.scale.linear()
                            .domain([0, 1])
                            .range([0, height + pady*2]);


    var court = d3.select(selector).selectAll('svg');

// Test: didn't work. I was trying not to repeat 3 times the same code.
//    var shot_types = ['F', 'B', 'S'];
//
//    for(var i = 0; i < shot_types.length; i++)
//    {
////        var filter_func = function(shot){
////            return shot.shot_type === shot_types[i];
////        };
//        court.append('g').attr('id', shot_types[i])
//            .selectAll('ellipse')
//            .data(data_shots
//                .filter(function(shot){
//                    return shot.shot_type === shot_types[i];
//                })
//            .enter()
//        .append('ellipse')
//        .append("svg:title")
//        .text(function(d) { return shot_type_verbose_names[d.shot_type]; });
//    }


    var forehands = court.append('g')
        .attr('id', 'F');
    var backhands = court.append('g')
        .attr('id', 'B');
    var serves = court.append('g')
        .attr('id', 'S');
    console.log(data_shots, 'data_shots');

    forehands.selectAll('ellipse')
        .data(data_shots
            .filter(function(shot){
                return shot.shot_type === 'F';
            }))
        .enter()
        .append('ellipse')
        .append("svg:title")
        .text(function(d) {
            var full_title = shot_type_verbose_names[d.shot_type].concat(d.serve_status).concat(d.number);
            return full_title; });


    backhands.selectAll('ellipse')
        .data(data_shots
            .filter(function(shot){
                return shot.shot_type === 'B';
            }))
        .enter()
        .append('ellipse')
        .append("svg:title")
        .text(function(d) { return shot_type_verbose_names[d.shot_type].concat(d.serve_status).concat(d.number); });

    serves.selectAll('ellipse')
        .data(data_shots
            .filter(function(shot){
                return shot.shot_type === 'S';
            }))
        .enter()
        .append('ellipse')
        .append("svg:title")
        .text(function(d) { return shot_type_verbose_names[d.shot_type].concat(d.serve_status).concat(d.number); });

    var ellipses = court.selectAll('ellipse');

    ellipses.transition()
        .duration(50)
        .delay(function(d, i) { return i * 400; })
        .attr('cx', function(d){return scale_point_x(d[attribute_to_draw + '_x']);})
        .attr('cy', function(d){return scale_point_y(d[attribute_to_draw + '_y']);})
        .attr('rx', 5)
        .attr('ry', 6)
        .attr('fill', 'yellow')
        .attr('stroke', 'orange')
        .attr('stroke-width', 1);

}


function get_data_shots(data_points){
    /**
     * Return all shots from every point in data_points in an array.
     */
    //data_points must be array-like.
    var i, n = data_points.length, a = [];
    for(i = 0; i < n; i++)
    {
        // Method to concatenate inplace: push.apply(array, newarray)
        a.push.apply(a, data_points[i].shots);
    }
    return a;
}

function draw_ellipses_master (selector, data, attribute_to_draw){
    var data_points = data.points;
    var data_shots = get_data_shots(data_points);

    function refresh_filter_data (selector) {
        function filter_data() {
            // setTimeout sets this to the global object, we need to save it.
            var this_saved = this;
            setTimeout(function (e) {
                //Each time one of the buttons is clicked we refilter everything.
                // Actually we just change the display to None to hide the points.

                var forehands = $(this_saved).find('#F').is(':checked');
                console.log(this_saved);
                var backhands = $(this_saved).find('#B').is(':checked');
                var serves = $(this_saved).find('#S').is(':checked');
                console.log(forehands);
                console.log(backhands);
                console.log(serves);
//                var allowed_shot_types =
//                    {
//                        'F': forehands,
//                        'B': backhands,
//                        'S': serves
//                    };
                //Ridiculous initialisation hack to avoid first character comma issues in selector.
                var shot_type_selector = 'g#Z';
                if (!forehands) {
                    shot_type_selector += ', g#F';
                }
                if (!backhands) {
                    shot_type_selector += ', g#B';
                }
                if (!serves) {
                    shot_type_selector += ', g#S';
                }

                d3.selectAll(selector)
                    .selectAll('g')
                    .style('display', 'inline');
                d3.selectAll(selector)
                    .selectAll(shot_type_selector)
                    .style('display', 'none');
            }, 100);
        }

        $(selector + ' .btn-group').click(filter_data);
    }
    draw_ellipses(selector, data_shots, attribute_to_draw);
    refresh_filter_data(selector, attribute_to_draw);
}
