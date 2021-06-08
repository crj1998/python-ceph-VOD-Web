String.format = function() {
    if (arguments.length == 0)
        return null;
    let str = arguments[0];
    for ( let i = 1; i < arguments.length; i++) {
        let re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
};

function createList(data){
    let t = "<li><div class='videolist' vpath='{0}' ipath='{1}'><div><img class='cover' src='{1}'/><img src='/static/images/play.png' class='videoed' /></div><h2><a href='#'>{2}</a></h2><p>{3}</p></div></li>";
    for (let i = 0; i < data["videos"].length; i++) {
        let v = data["videos"][i];
        $div = $(String.format(t, data["host"]+v["src"], data["host"]+v["cover"], v["title"], v["desc"]));
        $(".display").append($div);
    }
}



$().ready(function() {
    $(".switch_thumb").toggle(function() {
        $(this).addClass("swap");
        $("ul.display").fadeOut("fast", function() {
            $(this).fadeIn("fast").addClass("thumb_view");
        });
    }, function() {
        $(this).removeClass("swap");
        $("ul.display").fadeOut("fast", function() {
            $(this).fadeIn("fast").removeClass("thumb_view");
        });
    });
});


function closeplay() {
    let v = document.getElementById('video'); //获取视频节点
    $('.videos').hide(); //点击关闭按钮关闭暂停视频
    v.pause();
    $('.videos').html();
}

function addEvent(){
    $(".videolist").each(function() { //遍历视频列表
        $(this).hover(function() { //鼠标移上来后显示播放按钮
            $(this).find('.videoed').show();
        }, function() {
            $(this).find('.videoed').hide();
        });
        $(this).click(function() { //这个视频被点击后执行
            let t = "<video id='video' poster='{0}' style='width: 640px' src='{1}' preload='auto' controls='controls' autoplay='autoplay'></video><img onClick='closeplay()' class='vclose' src='/static/images/close.png' width='25' height='25'/>"
            let i = $(this).attr("ipath"); //获取视频预览图
            let v = $(this).attr("vpath"); //获取视频
            $(".videos").html(String.format(t, i, v));
            $(".videos").show();
        });
    });
}


$.getJSON("/videoslist", function(data){
    if (data["status"] == "ok"){
        createList(data["data"]);
        addEvent();
    } else{
        console.log("false");
    }

});
