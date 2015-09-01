function translate(x, y) {
    return 'translate(' + x + ',' + y + ')';
}

function define_court_data(selector) {
    // offset is the proportion len(bottom line) - len(net line)/2*len(net line)
    // service_square_end indicates where on the alley line segment the service
    // square ends, given the alley line is parametrized with 0 being the point
    // on the net line.
    //console.log(selector, 'selector in define court data');
    //console.log($(selector).width(), '$(selector).width() in define court data');
    var cw = 36,
        ch = 78/4,
        width = 0.9*$(selector).width(),// We take into account future padding.
        height = width * (ch / cw),
//        width = $(selector).innerWidth(),
//        height = $(selector).innerHeight(),
        padx = 0.05*$(selector).width(),
        pady = 0.10*width;

    var court_data = {
                 "cw": cw,
                 "ch": ch,
                 "width": width,
                 "height": height,
                 "padx": padx,
                 "pady": pady
             };
    return court_data;
}


function draw_court(selector) {

    // First we clean any previous drawing (avoid drawing x courts when we resize the window).
    d3.select(selector).selectAll('svg').remove();

    var court_data = define_court_data(selector);
    var cw = court_data['cw'],
        ch = court_data['ch'],
        width = court_data['width'],
        height = court_data['height'],
        padx = court_data['padx'],
        pady = court_data['pady'];

    var alley_ratio = 4.5 / 36,
        offset = 0.3,
        bottom_line_len = cw,
        net_line_len = bottom_line_len / (1 + 2 * offset),
        service_square_end = 10 / ch;

    var x = d3.scale.linear()
        .domain([0, cw]) // width of a court
        .range([0, width]);

    var y = d3.scale.linear()
        .domain([0, ch])
        .range([0, height]);

    //console.log($(selector).width(), '$(selector).width() before svg and g appending');

    var court = d3.select(selector).append('svg')
        .style('width', width + padx * 2)
        .style('height', height + pady * 2)
        .attr('width', "100%")
        .attr('height', "100%")
        //.attr('class', 'debug')
        .append('g')
        .attr('transform', translate(padx, pady));

    //console.log($(selector).width(), '$(selector).width() after svg and g appending');

    // baselines
    court.selectAll('line.baseline')
        .data([0, ch])
        .enter().append('line')
        .attr('class', 'baseline')
        .attr('class', 'Baseline')
        .attr('x1', function(d) {
            return x(offset * net_line_len * (ch - d) / ch);
        })
        .attr('x2', function(d) {
            return x((net_line_len * ( 1 + offset * (1 + d / ch))));
        })
        .attr('y1', y)
        .attr('y2', y);

    // sidelines
    court.selectAll('line.sideline')
        .data([
            {
                'x1': 0,
                'x2': offset*net_line_len
            },
            {
                'x1': alley_ratio*bottom_line_len,
                'x2': (offset + alley_ratio)*net_line_len
            },
            {
                'x1': bottom_line_len*(1 - alley_ratio),
                'x2': (offset + 1 - alley_ratio)*net_line_len
            },
            {
                'x1': bottom_line_len,
                'x2': (offset + 1)*net_line_len
            }
            ])
        .enter().append('line')
        .attr('class', 'sideline')
        .attr('x1', function(d) {
            return x(d.x1);
        })
        .attr('x2', function(d) {
            return x(d.x2);
        })
        .attr('y1', y(ch))
        .attr('y2', 0);

    // service boxes
    var service = [ch - service_square_end*ch];
    court.selectAll('line.service')
        .data(service)
        .enter()
      .append('line')
        .attr('class', 'service')
        .attr('x1', function(d) {
            return x((offset * net_line_len * (ch - d) / ch) + alley_ratio * net_line_len * (1 + (1 - service_square_end) * 2 * offset));
        }) // start at the alley
        .attr('x2', function(d) {
            return x((net_line_len * ( 1 + offset * (1 + d / ch)) - alley_ratio * net_line_len * (1 + (1 - service_square_end ) * 2 * offset)));
        }) // end at the opposite alley
        .attr('y1', y)
        .attr('y2', y);

    court.selectAll('line.center')
        .data(service)
        .enter()
      .append('line')
        .attr('class', 'center')
        .attr('x1', x(cw / 2.))
        .attr('x2', x(cw / 2.))
        .attr('y1', y)
        .attr('y2', y(0));

    // center marks
    court.selectAll('line.mark')
        .data([ch - 1])
        .enter()
      .append('line')
        .attr('class', 'mark')
        .attr('x1', x(bottom_line_len / 2))
        .attr('x2', x(bottom_line_len / 2))
        .attr('y1', y)
        .attr('y2', function (d) {
        return y(d) + y(1);
        });
//    console.log(bottom_line_len, 'bottom_line_len == cw (or should!)');
//    console.log(bottom_line_len / 2, 'bottom_line_len / 2');
//    console.log(width, 'width at time of this calculation');
//    console.log(x(bottom_line_len / 2), 'x center mark')
}


// zones
function zones (selector, percentages) {
    //console.log(percentages, 'percetanges in zones js function');
    var court_data = define_court_data(selector);
    var cw = court_data['cw'],
        ch = court_data['ch'],
        width = court_data['width'],
        height = court_data['height'],
        padx = court_data['padx'],
        pady = court_data['pady'];

    var alley_ratio = 4.5/36,
        offset = 0.3,
        bottom_line_len = cw,
        net_line_len = bottom_line_len / (1 + 2 * offset),
        service_square_end = 10 / ch;


    var x = d3.scale.linear()
    .domain([0, cw]) // width of a court
    .range([0, width]);

    var y = d3.scale.linear()
        .domain([0, ch])
        .range([0, height]);

    var court = d3.select(selector)
        .select("svg");

    //var x_grid = [padx / 2, padx + x(cw / 4), padx + x(3 * cw / 4 - 4.5), x(cw) + 3*padx/2];
    // Convention: a coordinate of 4 in the x_grid, y_grid indicates the percentage
    // should be displayed in the middle.
    var x_grid = [
            x(0) + padx/2,
            padx + x(cw / 4),
            padx + x(3 * cw / 4 - 4.5),
            x(cw) - padx,
            x(cw / 2)
    ];
    var y_grid = [
            y(ch / 2),
            pady / 2,
            pady + y(0.5 * service_square_end * ch),
            pady + y(1.5 * service_square_end * ch),
            3 * pady / 2 + y(ch)
    ];

    y_grid = y_grid.reverse();

    court.selectAll("text").remove();
    court.selectAll("text")
        .data(percentages)
        .enter()
        .append("text")
        .text(function (d){
            return d.percentage.toFixed(1) + "%";
        })
        .attr("x", function (d){
            return x_grid[d.x_pos];
        })
        .attr("y", function (d){
            return y_grid[d.y_pos];
        })
        .attr("font-family", "sans-serif")
        .attr("font-size", width*0.05)
        .attr("fill", "lightyellow")
//        .attr("stroke", "orange")
//        .attr("strokeWidth", 10)
        .append("svg:title")
        .text(function(d) {
            //return d.x_pos*10 + d.y_pos; //debug
            return d.count;
        });
}


function zones_serve (selector, zones_first_left, zones_first_right,
                      zones_second_left, zones_second_right) {
    // Selector is not the #court div anymore since the div width has changed
    // This causes issues with scaling so we select directly the svg, whose
    // width is the expected one (consistent with width in the draw_court
    // function).
//    console.log(zones_first_left, 'zones_first_left');
//    console.log(zones_first_right, 'zones_first_right');
    var court_data = define_court_data(selector);
    var cw = court_data['cw'],
        ch = court_data['ch'],
        width = court_data['width'],
        height = court_data['height'],
        padx = court_data['padx'],
        pady = court_data['pady'];

//    console.log(cw, 'cw');
//    console.log(width, 'width');
//    console.log(padx, 'padx');
//    console.log($(selector).width(), 'selector width');

    var alley_ratio = 4.5/36,
        offset = 0.3,
        bottom_line_len = cw,
        net_line_len = bottom_line_len / (1 + 2 * offset),
        service_square_end = 10 / ch;


    var x = d3.scale.linear()
    .domain([0, cw]) // width of a court
    .range([0, width]);

    var y = d3.scale.linear()
        .domain([0, ch])
        .range([0, height]);

    var court = d3.select(selector);
        //.select("svg");

    //var x_grid = [padx / 2, padx + x(cw / 4), padx + x(3 * cw / 4 - 4.5), x(cw) + 3*padx/2];
    // Convention: a coordinate of 4 in the x_grid, y_grid indicates the percentage
    // should be displayed in the middle.
    var x_grid = [
            padx,
            padx + x(cw / 4.5),
            padx + x(cw / 3.2),
            padx + x(cw / 2.4),
            padx + x(cw * 0.51),
            padx + x(cw * 0.51),
            padx + x(cw - cw / 2.6),
            padx + x(cw - cw / 3.6),
            padx + x(cw - cw / 4.5),
    ];

    var y_grid = [
            pady / 2,
            pady + y(0.8 * service_square_end * ch),
            pady + y(1.5 * service_square_end * ch),
    ];

    y_grid = y_grid.reverse();

    function draw_grid(x_grid, y_grid) {
        court.selectAll("line.x_grid")
        .data(x_grid)
        .enter()
        .append("line")
        .attr('class', 'x_grid')
        .attr("x1", function (d) {return d})
        .attr("y1", 0)
        .attr("x2", function (d) {return d})
        .attr("y2", height + 2 * pady);

        court.selectAll("line.y_grid")
        .data(y_grid)
        .enter()
        .append("line")
        .attr('class', 'y_grid')
        .attr("y1", function (d) {return d})
        .attr("x1", 0)
        .attr("y2", function (d) {return d})
        .attr("x2", width + 2 * padx);
    }
    //draw_grid(x_grid, y_grid);


    var zones_all_first = [];
    zones_all_first.push.apply(zones_all_first, zones_first_left);
    zones_all_first.push.apply(zones_all_first, zones_first_right);

    var zones_all_second = [];
    zones_all_second.push.apply(zones_all_second, zones_second_left);
    zones_all_second.push.apply(zones_all_second, zones_second_right);


    function write_percentages (zones) {
        court.selectAll("text")
            .data(zones)
            .enter()
            .append("text")
            .text(function (d){
                return d.percentage.toFixed(1) + "%";
            })
            .attr("x", function (d){
                return x_grid[d.x_pos];
            })
            .attr("y", function (d){
                return y_grid[d.y_pos];
            })
            .attr("font-family", "sans-serif")
            .attr("font-size", width*0.03)
            .attr("fill", "lightyellow")
    //        .attr("stroke", "orange")
    //        .attr("strokeWidth", 10)
            .append("svg:title")
            .text(function(d) {
                //return d.x_pos*10 + d.y_pos; //debug
                return d.count + ' premier' + ((d.count===1)?'':'s') + ' service' + ((d.count===1)?'':'s');});
    }

    function display_legend() {
        var legend_serves = [
            {'label': 'Premier service',
                'color_label': "lightyellow",
                'x': 0,
                'y': 1.5
            },
            {'label': 'Second service',
                'color_label': "darkgreen",
                'x': 0,
                'y': 3
            }
        ];

        court.selectAll("text.legend_serves")
            .data(legend_serves)
            .enter()
            .append("text")
            .text(function (d) {
                return 'X%: ' + d.label;
            })
            .attr("class", "legend_serve")
            .attr("x", function (d) {
                return x(d.x);
            })
            .attr("y", function (d) {
                return y(d.y);
            })
            .attr("font-family", "sans-serif")
            .attr("font-size", width*0.03)
            .attr("fill", function (d) {
                return d.color_label;
            });
        //console.log(legend_serves)
    }


    function write_percentages_second_serve (zones) {
        court.selectAll("text.second_serve")
            .data(zones)
            .enter()
            .append("text")
            .attr("class", "second_serve")
            .text(function (d){
                return d.percentage.toFixed(1) + "%";
            })
            .attr("x", function (d){
                return x_grid[d.x_pos];
            })
            .attr("y", function (d){
                return y_grid[d.y_pos] + 0.07 * height;
            })
            .attr("font-family", "sans-serif")
            .attr("font-size", width*0.03)
            .attr("fill", "darkgreen")
    //        .attr("stroke", "orange")
    //        .attr("strokeWidth", 10)
            .append("svg:title")
            .text(function(d) {
                //return d.x_pos*10 + d.y_pos; //debug
                return d.count + ' second' + ((d.count===1)?'':'s') + ' service' + ((d.count===1)?'':'s');
            });
    }

    court.selectAll("text").remove();
    write_percentages(zones_all_first);
    write_percentages_second_serve(zones_all_second);
    display_legend();

    // We draw the grid used in calculation for debugging purposes...
    // DOES NOT MAKE SENSE AS THE PADDING IS DIFFERENT.
        x_grid = $.map([0.1218423981082209,
 0.20615384615384616,
 0.42653846153846153,
 0.4891500904159132,
 0.5108499095840868,
 0.7938461538461539,
 0.5734615384615385,
 0.8781576018917792], function(d) {
            return padx + x(d * cw);
        });

    x_grid = $.map(
        [0.21153846153846156, 0.2692307692307693, 0.4423076923076923, 0.5,
            0.5, 0.7307692307692307, 0.5576923076923077, 0.7884615384615384],
        function(d) {
            return d * $(selector).width();
        });
    //draw_grid(x_grid, y_grid)
}

/*function resize(selector) {
    *//* Find the new window dimensions *//*
    var width = parseInt(d3.select(selector).style("width")),
        height = parseInt(d3.select(selector).style("height"));




*//*
    *//**//* Update the range of the scale with new width/height *//**//*
    xScale.range([0, width]).nice(d3.time.year);
    yScale.range([height, 0]).nice();

    *//**//* Update the axis with the new scale *//**//*
    graph.select('.x.axis')
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    graph.select('.y.axis')
      .call(yAxis);

    *//**//* Force D3 to recalculate and update the line *//**//*
    graph.selectAll('.line')
      .attr("d", line);*//*
}*/

