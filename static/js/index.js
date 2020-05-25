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

    })
    
   

function log_text(data) {
    $.ajax({
        url: "./ml/prediction",
        type: "POST",
        // dataType: 'json', 
        // contentType: 'application/json;charset=UTF-8',    
        data: JSON.stringify(data)
    }).done(function (result)
    
    { $("#rating_text").text(result['result']) })
}
    

        