document.addEventListener('DOMContentLoaded', function () {
	chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    var url0 = tabs[0].url;
    $("#msgLabel").text(url0);
    $.ajax( {              // Flask中获取数据的function的url
        type: "POST",
        url: "http://localhost:5000/dataconvector",
        crossDomain:true,
        data: JSON.stringify({"url":url0}),
        dataType:"JSON"
    }).done(function(responseData){
        var a=responseData.result
        $("#result").text(a);
    });
    

    });
});
