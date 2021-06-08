var remember_key = document.getElementById("remember_key");
var ak = document.getElementById("ak");
var sk = document.getElementById("sk");

// remember key
window.onload = function (){
    // get ak from cookie
    let access_key = getCookie("AK") ;
    if (access_key == ""){
        ak.value="" ;
        sk.value="" ;
        remember_key.checked = false ;
    }
    else{
        let secret_key = getCookie("SK") ;
        ak.value = access_key ;
        sk.value = secret_key ;
        remember_key.checked = true ;
    }
}
function getCookie(name){
    var arr,reg = new RegExp("(^| )"+name+"=([^;]*)(;|$)");
    if(arr=document.cookie.match(reg)){return unescape(arr[2]);}
    else{return null;}

}
function delCookie(name){
    let exp = new Date();
    exp.setTime(exp.getTime() - 1);
    let cval = getCookie(name);
    if(cval!=null){document.cookie= name + "="+cval+";expires="+exp.toGMTString();}
}
function setCookie(name, value){
    let exp = new Date();
    exp.setTime(exp.getTime() + 7*24*60*60*1000);
    document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
}
function success(data, textStatus, jqXHR){
    if (data["status"] == "ok"){
        if (remember_key.checked == true ){
            setCookie("AK", ak.value);
            setCookie("SK", sk.value);
        }  else {
            delCookie("AK");
            delCookie("SK");
        };
        setTimeout(function(){
            window.location.href = "/player"
        }, 1000)
    } else{
        alert(data["errmsg"])
    }
}
function login() {
    let access_key = ak.value;
    let secret_key = sk.value;
    if(!access_key || !secret_key){ //拦截空内容
        alert("Empty Key")
    } else{
        $.ajax({
          type: "POST",
          url: "/login",
          data: {"ak": access_key, "sk": secret_key},
          success: success,
        });
    }
}