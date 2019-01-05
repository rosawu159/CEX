document.addEventListener('DOMContentLoaded', function () {
	chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    var url0 = tabs[0].url;
    $("#msgLabel").text(url0);
    $.ajax( {              // Flask中获取数据的function的url
        type: "POST",
        url: "http://localhost:5000/dataconvector",
        crossDomain:true,
        data: JSON.stringify({"url":url0}),
        dataType:"JSON",
        beforeSend: function(){
            $("#text").text("正在計算網站的不信任指數...");
            $("#loadingIMG").show();
            
        }
    }).done(function(responseData){
        var a=responseData.result
        var score=a*20+5
        $("#text").text("此網站的不信任指數為");
        $("#result").text(score+"%");
        $("#loadingIMG").hide();
        var img = document.createElement("img");
        if (a<=1){
            img.src = "0.png";}
        else if(a>1 && a<=2){
            img.src = "1.png";}
        else if(a>2 && a<=3){
            img.src = "2.png";}
        else if(a>3 && a<=4){
            img.src = "3.png";}
        else if(a>4 && a<=5){
            img.src = "4.png";}
        
        var src = document.getElementById("emoji");
        src.appendChild(img);
    });
    

    });
});
