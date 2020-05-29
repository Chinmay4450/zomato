$('body')
  .on("click", "#submit_btn", function () {
    console.log("clicked")
    var dict = {}
    dict["first"] = $("#loca").val()
    dict["second"] = $("#avg").val()
    dict["third"] = $("#booking").val()
    dict["fourth"] = $("#onlined").val()
    dict["fifth"] = $("#dilivering").val()
    log_text(dict)

    plot_all_charts(dict["first"])
  })



function log_text(data) {
  $.ajax({
    url: "./ml/prediction",
    type: "POST",
    data: JSON.stringify(data)
  }).done(function (result) {
    $("#rating_text").text(result['result'])
  })
}

function plot_all_charts(location) {
  $.ajax({
    url: "./ml/famousmenu/" + location,
    type: "GET",
    async: false
  }).done(function (result) {
    console.log(result);
    $("#famous_chart").attr("src", result.img)
  })
  $.ajax({
    url: "./ml/onlinedelivery/" + location,
    type: "GET",
    async: false
  }).done(function (result) {
    console.log(result);
    $("#online_chart").attr("src", result.img)
  })
  $.ajax({
    url: "./ml/tablebooking/" + location,
    type: "GET",
    async: false
  }).done(function (result) {
    console.log(result);
    $("#table_chart").attr("src", result.img)
  })
  $.ajax({
    url: "./ml/deliveringnow/" + location,
    type: "GET",
    async: false
  }).done(function (result) {
    console.log(result);
    $("#delivering_chart").attr("src", result.img)
  })
}

