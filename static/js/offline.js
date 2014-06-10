/* 系统维护中，动态提示函数 */
$(document).ready(function(){
	window.setInterval(offline_timer, 1000);
});



// offline计时轮询器
var index = 3;
function offline_timer(){
    var offline_dom = $('#offline_id');
    index += 1;
    if ((index % 3) == 0){
        offline_dom.text('The system is offline，please try again later..');
    } else if ((index % 3) == 1){
        offline_dom.text('The system is offline，please try again later....');
    } if ((index % 3) == 2){
        offline_dom.text('The system is offline，please try again later......');
    }
}