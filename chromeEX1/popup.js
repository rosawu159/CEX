document.addEventListener('DOMContentLoaded', function () {
	chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    var url0 = tabs[0].url;
    $("#msgLabel").text(url0);
    $.ajax( {              
        type: "POST",
        url: "http://localhost:5000/dataconvector",
        crossDomain:true,
        data: JSON.stringify({"url":url0}),
        dataType:"JSON",
        beforeSend: function(){
            $("#text").text("正在計算網站的不信任指數...？？？");
            $("#loadingIMG").show();
            
        }
    }).done(function(responseData){
        var a=responseData.result[3]
        var score=a*20
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

        var update=responseData.result[0]
        var expire=responseData.result[1]
        var company=responseData.result[2]

        if(update == "0" || company == "0"){
            $("#description1").text("未取得相關公司資訊");
            $("#description2").text("無法得知最後更新與到期日期");        
        }
        else{
            $("#description1").text("公司名稱："+company);
            $("#description2").text("最後更新日期："+update);
            $("#description3").text("到期日期："+expire);


        }

    });
    

    });
});
