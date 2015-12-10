var DISCIPLINE_COLORS = {
  'Arts & humanities': '#8dd3c7',
  'Engineering': '#bc80bd',
  'Mathematical science': '#ccebc5',
  'Language': '#fb8072',
  'Natural science': '#80b1d3',
  'Other': '#fdb462',
  'Professional': '#fccde5',
  'Social science': '#b3de69'
};

var dotChart = function(data, container) {
  // Global vars
  var containerElement;
  var chartElement;
  var labelColumn = 'sub';
  var valueColumn = 'avg';

  var barHeight = 20;
  var barGap = 3;
  var labelWidth = 160;
  var labelMargin = 20;
  var valueMinWidth = 30;
  var dotRadius = 5;
  var transitionDuration = 1000;
  var margins = {
      top: 30,
      right: 20,
      bottom: 0,
      left: (labelWidth + labelMargin)
  };

  if (isMobile) {
    labelWidth = 120;
    labelMargin = 10;
    margins['left'] = labelWidth + labelMargin
  }

  var statsTemplate = _.template($('#stats-template').html());

  var colors = DISCIPLINE_COLORS;

  /*
   * Render the graphic
   */
  var render = function(data, container) {
      // Set up resize event listener
      $( window ).resize(function() {
          renderDotChart({
              container: container,
              data: data
          });
      });

      // Render the chart!
      renderDotChart({
          container: container,
          data: data
      });
  }

  /*
   * Render a dot chart.
   */
  var renderDotChart = function(config) {
      config['width'] = $(config['container']).width();

      /*
       * Setup
       */

      var ticksX = 4;
      var roundTicksFactor = 1;

      // Calculate actual chart dimensions
      var chartWidth = config['width'] - margins['left'] - margins['right'];
      var chartHeight = ((barHeight + barGap) * config['data'].length);

      // Clear existing graphic (for redraw)
      containerElement = d3.select(config['container']);
      containerElement.html('');

      var legendContainer = d3.select('#legend-container');
      legendContainer.html('');

      /*
       * Render a color legend.
       */

      var legend = legendContainer.append('ul')
          .attr('class', 'key')
          .style('width', config['width'] + 'px')
          .selectAll('g')
              .data(_.pairs(colors))
          .enter().append('li')
          .attr('class', 'key-item')
      legend.append('b')
          .style('background-color', function(d) {
            return d[1];
          });

      legend.append('label')
          .text(function(d) {
              return d[0];
          });

      /*
       * Create the root SVG element.
       */
      var chartWrapper = containerElement.append('div')
          .attr('class', 'graphic-wrapper');

      chartElement = chartWrapper.append('svg')
          .attr('width', chartWidth + margins['left'] + margins['right'])
          .attr('height', chartHeight + margins['top'] + margins['bottom'])
          .append('g')
          .attr('transform', 'translate(' + margins['left'] + ',' + margins['top'] + ')');

      /*
       * Create D3 scale objects.
       */
      var xScale = d3.scale.linear()
          .domain([2.5, 4])
          .range([0, chartWidth]);

      /*
       * Create D3 axes.
       */
      var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient('bottom')
          .ticks(ticksX)
          .tickFormat(function(d) {
              return d;
          });

      var onTargetHover = function(d) {
        d3.selectAll('.hover-target rect').classed('hover', false);
        $('#stats').html(statsTemplate(d));
        gradeHistogram(d.dist, '#histogram');
      }

      /* Render hover targets */
      chartElement.append('g')
          .attr('class', 'hover-target')
          .selectAll('rect')
          .data(config['data'])
          .enter().append('rect')
              .attr('x', function(d, i) {
                  return -margins['left'];
              })
              .attr('y', function(d, i) {
                  return i * (barHeight + barGap);
              })
              .attr('width', chartWidth + margins['left'])
              .attr('height', barHeight)
              .attr('fill', '#fff')
              .attr('id', function(d) { return d.slug })
          .on('mouseover', function(d) {
            if (!isMobile) {
              onTargetHover(d);
              d3.select(this).classed('hover', true);
            }
          });

      /*
       * Render axes to chart.
       */
      chartElement.append('g')
          .attr('class', 'x axis')
          //.attr('transform', makeTranslate(0, chartHeight))
          .call(xAxis)
          .selectAll('text')
            .attr('transform', 'translate(0,-25)');
        

      /*
       * Render grid to chart.
       */
      var xAxisGrid = function() {
          return xAxis;
      };

      chartElement.append('g')
          .attr('class', 'x grid')
          .attr('transform', makeTranslate(0, chartHeight))
          .call(xAxisGrid()
              .tickSize(-chartHeight, 0, 0)
              .tickFormat('')
          );

      /*
       * Render dots to chart.
       */
      chartElement.append('g')
          .attr('class', 'dots')
          .selectAll('circle')
          .data(config['data'])
          .enter().append('circle')
              .attr('cx', function(d, i) {
                  return xScale(d[valueColumn]);
              })
              .attr('cy', function(d, i) {
                  return i * (barHeight + barGap) + (barHeight / 2);
              })
              .attr('r', dotRadius)
              .attr('fill', function(d) {
                  return colors[d['discipline']];
              });

      /*
       * Render labels.
       */
      chartWrapper
          .append('ul')
          .attr('class', 'labels')
          .attr('style', formatStyle({
              'width': labelWidth + 'px',
              'top': margins['top'] + 'px',
              'left': '0'
          }))
          .selectAll('li')
          .data(config['data'])
          .enter()
          .append('li')
              .attr('style', function(d, i) {
                  return formatStyle({
                      'width': labelWidth + 'px',
                      'height': barHeight + 'px',
                      'left': '0px',
                      'top': i * (barHeight + barGap) + 'px;'
                  });
              })
              .attr('class', function(d) {
                  return classify(d[labelColumn]);
              })
              .append('span')
                  .text(function(d) {
                      return d[labelColumn];
                  });

      /*
       * Render dot values.
       */
      chartElement.append('g')
          .attr('class', 'value')
          .selectAll('text')
          .data(config['data'])
          .enter().append('text')
              .attr('x', function(d, i) {
                  return xScale(d[valueColumn]) + 10;
              })
              .attr('y', function(d,i) {
                  return i * (barHeight + barGap) + (barHeight / 2) + 3;
              })
              .text(function(d) {
                  return d[valueColumn].toFixed(2);
              });
  }

  var sortByAverage = function() {
    _.each(['circle','.labels li', '.value text', '.hover-target rect'], function(cls) {
      containerElement.selectAll(cls)
        .sort(function(a, b) {
          return a['avg'] - b['avg'];
      });
    });

    animateTransition();
  }

  var sortAlphabetical = function() {
    _.each(['circle','.labels li', '.value text', '.hover-target rect'], function(cls) {
      containerElement.selectAll(cls)
        .sort(function(a, b) {
          return a['sub'] == b['sub'] ? 0 : a['sub'] < b['sub'] ? -1 : 1;
      });
    });

    animateTransition();
  }

  var sortByDiscipline = function() {
    _.each(['circle','.labels li', '.value text', '.hover-target rect'], function(cls) {
      containerElement.selectAll(cls)
        .sort(function(a, b) {
          return a['discipline'] == b['discipline'] ? 0 : a['discipline'] < b['discipline'] ? -1 : 1;
      });
    });

    animateTransition();
  }

  var sortByCount = function() {
    _.each(['circle','.labels li', '.value text', '.hover-target rect'], function(cls) {
      containerElement.selectAll(cls)
        .sort(function(a, b) {
          return b['num'] - a['num'];
      });
    });

    animateTransition();
  }

  var animateTransition = function() {
    chartElement.selectAll('circle')
      .transition()
      .duration(transitionDuration)
      .attr('cy', function(d, i) {
        return i * (barHeight + barGap) + (barHeight / 2);
      });

    containerElement.selectAll('.labels li')
      .transition()
      .duration(transitionDuration)
      .attr('style', function(d, i) {
          return formatStyle({
              'width': labelWidth + 'px',
              'height': barHeight + 'px',
              'left': '0px',
              'top': i * (barHeight + barGap) + 'px;'
          });
      });

    containerElement.selectAll('.value text')
      .transition()
        .duration(transitionDuration)
        .attr('y', function(d,i) {
            return i * (barHeight + barGap) + (barHeight / 2) + 3;
        });

    containerElement.selectAll('.hover-target rect')
      .attr('y', function(d,i) {
          return i * (barHeight + barGap);
      });

    return true;
  }
  
  var toggleSort = function(sortBy) {
    if (sortBy == 'Average') {
      sortByAverage();
    } else if (sortBy == 'Alphabetical') {
      sortAlphabetical();
    } else if (sortBy == 'Discipline') {
      sortByDiscipline();
    } else if (sortBy == 'Number of grades') {
      sortByCount();
    }
  }

  $(document).ready(function() {
    $(".dropdown-button").click(function() {
      var $button, $menu;
      $button = $(this);
      $menu = $button.siblings(".dropdown-menu");
      $menu.toggleClass("show-menu");
      $menu.children("li").click(function() {
        $menu.removeClass("show-menu");
        $button.html($(this).html());
        toggleSort($(this).html());
      });
    });
  });

  /*
   * Initially render the graphic
   */
  render(data, container);
};