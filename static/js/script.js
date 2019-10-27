$(document).ready(function () {
    $('.sidenav').sidenav();

    // Force reload of script.js to override caching
    // Stack Overflow
    //https://stackoverflow.com/questions/50276601/avoid-javascript-css-caching
    let resourcePath = 'static/js/script.js';
    document.getElementById('myScript').src = resourcePath + '?v=' + Date.now();

        let res = JSON.parse($("#resList").text());
        //Make graph for poll results
        
        window.onload = makeGraph(res);

        function makeGraph(results) {

            //From CI Lesson
            let ndx = crossfilter(results);
            let guitar_dim = ndx.dimension(dc.pluck("_id"));
            let votes_dim = guitar_dim.group().reduceSum(dc.pluck("number_of_votes"));

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
        }
});