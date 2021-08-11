function sendData(){

    var values = [];
    var fields = document.getElementsByName("mytext[]");
    for(var i = 0; i < fields.length; i++) {
        values.push(fields[i].value);
    }

    for(var i = 0; i < values.length; i++){
        if(values[i] == ""){
            newAlert("triangle", "warning", "Request not sent", "1000", "True");
            return;
        }
    }

    $.ajax({
        type: "POST",
        url: '/get_post_json',
        contentType: "application/json",
        data: JSON.stringify({values}),
        dataType: "json",
        success: function(response) {
            console.log(response);
        },
        error: function(err) {
            console.log(err);
        }
    });

    newAlert("check", "success", "Request sent succesfully", "1000", "True");
    //window.location.href = "http://localhost:5000/test";
};
/*
$(document).ready(function() {
    $('data').submit(function() {
        e.preventDefault();
        var values = [];
        var fields = document.getElementsByName("mytext[]");
        for(var i = 0; i < fields.length; i++) {
            values.push(fields[i].value);
        }

        for (var i = 0; i < values.length; i++) {
            if(values[i] == ""){
                console.log("1");
                return;
            }
        }
        console.log("2");
        $.ajax({
            type: "POST",
            url: '/get_post_json',
            contentType: "application/json",
            data: JSON.stringify({values}),
            dataType: "json",
            success: function(response) {
                console.log(response);
            },
            error: function(err) {
                console.log(err);
            }
        });
    });
});*/