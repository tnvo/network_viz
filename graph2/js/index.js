var chart = AmCharts.makeChart("chartdiv", {
  "type": "serial",
  "theme": "light",
  "columnWidth": 1,
  "dataProvider": [{
    "category": "1",
    "count": 25
  }, {
    "category": "2-5",
    "count": 81
  }, {
    "category": "5-100",
    "count": 73
  }, {
    "category": "100-200",
    "count": 40
  },
                  {
    "category": "200-1000",
    "count": 30
  },
                   {
    "category": "<1000",
    "count": 70
  }
                  ],
  "graphs": [{
    "fillColors": "#c55",
    "fillAlphas": 0.9,
    "lineColor": "#fff",
    "lineAlpha": 0.7,
    "type": "column",
    "valueField": "count"
  }],
  "categoryField": "category",
  "categoryAxis": {
    "startOnAxis": true,
    "title": "Try"
  },
  "valueAxes": [{
    "title": "Count"
  }]
});
