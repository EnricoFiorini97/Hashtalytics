google.charts.load('current', {'packages': ['line']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Day', '#Trend'],
        ['Lun', 15000],
        ['Mar', 12070],
        ['Mer', 16060],
        ['Gio', 10030],
        ['Ven', 11870],
        ['Sab', 27660],
        ['Dom', 1000],
    ]);

    var options = {
        title: 'Andamento trend',
        curveType: 'function',
        legend: {position: 'bottom'}
    };

    var chart = new google.charts.Line(document.getElementById('graph'));
    chart.draw(data, google.charts.Line.convertOptions(options));
}