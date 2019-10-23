$(document).ready(function () {
    $('.sidenav').sidenav();

    //Make graph for poll results - dummy values below
    var results = [{
            "guitar_name":"strat", "votes": 12
        },
        {
            "guitar_name":"lesPaul", "votes": 5
        },
        {
            "guitar_name": "xguitar", "votes": 7
        },
    ];


    //From CI Lesson
    let ndx = crossfilter(results);
    let guitar_dim = ndx.dimension(dc.pluck("guitar_name"));
    let votes_dim = guitar_dim.group().reduceSum(dc.pluck("votes"));

        dc.barChart("#pollChart")
        .width(300)
        .height(150)
        .margins({
            top: 10,
            right: 50,
            bottom: 30,
            left: 50
        })
        .dimension(guitar_dim)
        .group(votes_dim)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .xAxisLabel("votes")
        .yAxis().ticks(4);

    dc.renderAll();
});