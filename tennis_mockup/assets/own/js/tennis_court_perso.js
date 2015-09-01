/*global d3:False */

function translate(x, y) {
    return 'translate(' + x + ',' + y + ')';
}

function define_court_data() {
    var cw = 36,
        ch = 78,
        width = 200,
        height = width * (ch / cw),
        padx = 0.15*width,
        pady = 0.225*width;
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
    //Would be nice to be able to pass the variables as a dictionary to the next-level functions.

    var court_data = define_court_data();
    var cw = court_data['cw'],
        ch = court_data['ch'],
        width = court_data['width'],
        height = court_data['height'],
        padx = court_data['padx'],
        pady = court_data['pady'];


    var x = d3.scale.linear()
        .domain([0, cw]) // width of a court
        .range([0, width]);

    var y = d3.scale.linear()
        .domain([0, ch])
        .range([0, height]);

    var court = d3.select(selector).append('svg')
        .style('width', width + padx * 2)
        .style('height', height + pady * 2)
        .attr('width', "100%")
        .attr('height', "100%")
        .attr('class', 'debug')
        .append('g')
        .attr('transform', translate(padx, pady));

    // baselines
    court.selectAll('line.baseline')
        .data([0, ch / 2, ch])
        .enter().append('line')
        .attr('class', 'baseline')
        .attr('class', 'Baseline')
        .attr('x1', 0)
        .attr('x2', x(cw))
        .attr('y1', y)
        .attr('y2', y);

    // sidelines
    court.selectAll('line.sideline')
        .data([0, 4.5, cw - 4.5, cw])
        .enter().append('line')
        .attr('class', 'sideline')
        .attr('x1', x)
        .attr('x2', x)
        .attr('y1', 0)
        .attr('y2', y(ch));

    // service boxes
    var service = [ch / 2 + 21, ch / 2 - 21];
    court.selectAll('line.service')
        .data(service)
        .enter()
      .append('line')
        .attr('class', 'service')
        .attr('x1', x(4.5)) // start at the alley
    .attr('x2', x(cw - 4.5)) // end at the opposite alley
    .attr('y1', y)
        .attr('y2', y);

    court.selectAll('line.center')
        .data(service)
        .enter()
      .append('line')
        .attr('class', 'center')
        .attr('x1', x(cw / 2))
        .attr('x2', x(cw / 2))
        .attr('y1', y)
        .attr('y2', y(ch / 2));

    // center marks
    court.selectAll('line.mark')
        .data([0, ch - 1])
        .enter()
      .append('line')
        .attr('class', 'mark')
        .attr('x1', x(cw / 2))
        .attr('x2', x(cw / 2))
        .attr('y1', y)
        .attr('y2', function (d) {
        return y(d) + y(1);
        });

    // We define a zone with the bottom left and top right corner.
    // First service square
    var zone_1 = [
        {
            'x': x(cw / 2),
            'y': y(ch / 2)
        },
        {
            'x': x(0),
            'y': y(ch/2 + 21)
        }
    ];
    var zone_2 = [
        {
            'x': x(cw / 2),
            'y': y(ch / 2)
        },
        {
            'x': x(0),
            'y': y(ch/2 + 21)
        }
    ];
    var zone_3 = [
        {
            'x': x(0),
            'y': y(cw)
        },
        {
            'x': x(cw/2),
            'y': y(ch/2 + 21)
        }
    ];



    // We decide where we will write the percentages.
    var percentage_position = [(x(cw/4), y(ch)), (x(3*cw/4), y(ch)), (x(cw/2), y(ch/2))]
        var service = [ch / 2 + 21, ch / 2 - 21];



}

// zones
function zones (selector, percentages) {
    var court_data = define_court_data();
    var cw = court_data['cw'],
        ch = court_data['ch'],
        width = court_data['width'],
        height = court_data['height'],
        padx = court_data['padx'],
        pady = court_data['pady'];

    var x = d3.scale.linear()
    .domain([0, cw]) // width of a court
    .range([0, width]);

    var y = d3.scale.linear()
        .domain([0, ch])
        .range([0, height]);

    var court = d3.select(selector)
        .select("svg");

    //var x_grid = [padx / 2, padx + x(cw / 4), padx + x(3 * cw / 4 - 4.5), x(cw) + 3*padx/2];
    var x_grid = [x(0) + padx/2, padx + x(cw / 4), padx + x(3 * cw / 4 - 4.5), x(cw) + padx/2];
    var y_grid = [pady / 2, pady + y(ch / 7), pady + y(ch / 2 - 21/2), pady + y(ch / 2 + 5)];

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
        .attr("font-size", "11px")
        .attr("fill", "black");
}

