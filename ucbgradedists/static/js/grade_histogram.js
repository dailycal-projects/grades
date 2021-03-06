// Global config
var GRAPHIC_DEFAULT_WIDTH = 600;
var MOBILE_THRESHOLD = 500;

// D3 formatters
var fmtComma = d3.format(',');

var gradeHistogram = function(data, container) {
    /*
     * Format graphic data for processing by D3.
     */
    var formatHistogramData = function(data) {
        var graphicData = _.sortBy(data, function(d) {
          var value = 0;
          var letter = d.label[0];

          if (letter == 'F') {
            value = 40;
          } else if (letter == 'D') {
            value = 30;
          } else if (letter == 'C') {
            value = 20;
          } else if (letter == 'B') {
            value = 10;
          } else if (letter == 'A') {
            value = 0;
          }

          if (d.label.length > 0) {
            var suffix = d.label[1];
            if (suffix == '+') {
              value -= 1;
            } else if (suffix == '-') {
              value += 1;
            }
          } 

          return value;
        });

        return graphicData;
    }

    /*
     * Render the graphic.
     */
    var renderHistogram = function(data, container) {
        var graphicData = formatHistogramData(data);

        // Set up resize event listener
        $( window ).resize(function() {
            renderColumnChart({
                container: container,
                data: graphicData
            });
        });

        // Render the chart
        renderColumnChart({
            container: container,
            data: graphicData
        });
    }

    /*
     * Render a column chart.
     */
    var renderColumnChart = function(config) {
        /* Get width of histogram */
        config['width'] = $(config['container']).width()

        /*
         * Set up chart container.
         */
        var labelColumn = 'label';
        var valueColumn = 'amt';

        var aspectWidth = 4;
        var aspectHeight = 3;
        var valueGap = 6;

        var margins = {
            top: 5,
            right: 5,
            bottom: 20,
            left: 50
        };

        var ticksY = 4;
        var roundTicksFactor = 10;

        // Calculate actual chart dimensions
        var chartWidth = config['width'] - margins['left'] - margins['right'];
        var chartHeight = Math.ceil((config['width'] * aspectHeight) / aspectWidth) - margins['top'] - margins['bottom'];

        // Clear existing graphic (for redraw)
        var containerElement = d3.select(config['container']);
        containerElement.html('');

        /*
         * Create the root SVG element.
         */
        var chartWrapper = containerElement.append('div')
            .attr('class', 'graphic-wrapper');

        var chartElement = chartWrapper.append('svg')
            .attr('width', chartWidth + margins['left'] + margins['right'])
            .attr('height', chartHeight + margins['top'] + margins['bottom'])
            .append('g')
            .attr('transform', 'translate(' + margins['left'] + ',' + margins['top'] + ')');

        /*
         * Create D3 scale objects.
         */
        var xScale = d3.scale.ordinal()
            .rangeRoundBands([0, chartWidth], .1)
            .domain(config['data'].map(function (d) {
                return d[labelColumn];
            }));

        var min = d3.min(config['data'], function(d) {
            return Math.floor(d[valueColumn] / roundTicksFactor) * roundTicksFactor;
        });

        if (min > 0) {
            min = 0;
        }

        var max = d3.max(config['data'], function(d) {
            return Math.ceil(d[valueColumn] / roundTicksFactor) * roundTicksFactor;
        });

        if (max < 50) {
            max = 50;
        }

        var yScale = d3.scale.linear()
            .domain([
                min,
                max
            ])
            .range([chartHeight, 0]);

        /*
         * Create D3 axes.
         */
        var xAxis = d3.svg.axis()
            .scale(xScale)
            .orient('bottom')
            .tickFormat(function(d, i) {
                return d;
            });

        var yAxis = d3.svg.axis()
            .scale(yScale)
            .orient('left')
            .ticks(ticksY)
            .tickFormat(function(d) {
                return d + '%';
            });

        /*
         * Render axes to chart.
         */
        chartElement.append('g')
            .attr('class', 'x axis')
            .attr('transform', makeTranslate(0, chartHeight))
            .call(xAxis);

        chartElement.append('g')
            .attr('class', 'y axis')
            .call(yAxis)

        /*
         * Render grid to chart.
         */
        var yAxisGrid = function() {
            return yAxis;
        };

        chartElement.append('g')
            .attr('class', 'y grid')
            .call(yAxisGrid()
                .tickSize(-chartWidth, 0)
                .tickFormat('')
            );

        /*
         * Render bars to chart.
         */
        chartElement.append('g')
            .attr('class', 'bars')
            .selectAll('rect')
            .data(config['data'])
            .enter()
            .append('rect')
                .attr('x', function(d) {
                    return xScale(d[labelColumn]);
                })
                .attr('y', function(d) {
                    if (d[valueColumn] < 0) {
                        return yScale(0);
                    }

                    return yScale(d[valueColumn]);
                })
                .attr('width', xScale.rangeBand())
                .attr('height', function(d) {
                    if (d[valueColumn] < 0) {
                        return yScale(d[valueColumn]) - yScale(0);
                    }

                    return yScale(0) - yScale(d[valueColumn]);
                })
                .attr('class', function(d) {
                    return 'bar bar-' + d[labelColumn];
                });

        /*
         * Render 0 value line.
         */
        chartElement.append('line')
            .attr('class', 'zero-line')
            .attr('x1', 0)
            .attr('x2', chartWidth)
            .attr('y1', yScale(0))
            .attr('y2', yScale(0));

        /*
         * Render bar values.
         */
        chartElement.append('g')
            .attr('class', 'value')
            .selectAll('text')
            .data(config['data'])
            .enter()
            .append('text')
                .text(function(d) {
                    return d[valueColumn].toFixed(0) + '%';
                })
                .attr('x', function(d, i) {
                    return xScale(d[labelColumn]) + (xScale.rangeBand() / 2);
                })
                .attr('y', function(d) {
                    return yScale(d[valueColumn]);
                })
                .attr('dy', function(d) {
                    var textHeight = d3.select(this).node().getBBox().height;
                    var barHeight = 0;

                    if (d[valueColumn] < 0) {
                        barHeight = yScale(d[valueColumn]) - yScale(0);

                        if (textHeight + valueGap * 2 < barHeight) {
                            d3.select(this).classed('in', true);
                            return -(textHeight - valueGap / 2);
                        } else {
                            d3.select(this).classed('out', true)
                            return textHeight + valueGap;
                        }
                    } else {
                        barHeight = yScale(0) - yScale(d[valueColumn]);

                        if (textHeight + valueGap * 2 < barHeight) {
                            d3.select(this).classed('in', true)
                            return textHeight + valueGap;
                        } else {
                            d3.select(this).classed('out', true)
                            return -(textHeight - valueGap / 2);
                        }
                    }
                })
                .attr('text-anchor', 'middle')
    }

    renderHistogram(data, container);
}
