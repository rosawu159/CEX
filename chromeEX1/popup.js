document.addEventListener('DOMContentLoaded', function () {
	chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    var url0 = tabs[0].url;
    $("#msgLabel").text(url0);
    $.ajax({
        url: "http://130.211.255.166/d",
        type:"GET",
        data:{q: url0,
            format:"json"},
        dataType: "JSONP",
        jsonp: false, 
        success: function(data){
            console.log(data)
        }
    })   
    });
});
