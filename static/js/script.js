$(document).ready(function () {
    $('.sidenav').sidenav();

    // Force reload of script.js to override caching
    // Stack Overflow
    //https://stackoverflow.com/questions/50276601/avoid-javascript-css-caching
    let resourcePath = 'static/js/script.js';
    document.getElementById('myScript').src = resourcePath + '?v=' + Date.now();

    let thisPage = $(location).attr("href")
    let thisPageLast = thisPage.substring(thisPage.length-7, thisPage.length)

    if (thisPageLast === "results") {
        //get data for graph from hidden div - NOT IDEAL 
        let res = JSON.parse($("#resList").text());
        window.onload = makeGraph(res);
    }

        //Make graph for poll results
         function makeGraph(results) {

        //From CI Lesson
        let ndx = crossfilter(results);
        let guitarDim = ndx.dimension(dc.pluck("_id"));
        let votesDim = guitarDim.group().reduceSum(dc.pluck("number_of_votes"));

        dc.barChart("#pollChart")
            //.width(300)
            //.height(150)
            /*
            .margins({
                top: 10,
                right: 50,
                bottom: 30,
                left: 50
            })
            */
            .dimension(guitarDim)
            .group(votesDim)
            .transitionDuration(500)
            .x(d3.scale.ordinal())
            .xUnits(dc.units.ordinal)
            .xAxisLabel("votes")
            .yAxis().ticks(4);

        dc.renderAll();
    }
});