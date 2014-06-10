/* 首页轮换 及 推荐产品翻页 */
$(document).ready(function(){
	window.setInterval(banner_timer, 2000);
});

// banner计时轮询器
function banner_timer(){
    var count = parseInt($('#banner_pic').find('a').length);
    var pos_px = $('#banner_pic').css('top');
    pos_px = parseInt(pos_px.substr(0, pos_px.indexOf('px')));
    var total_pos_px = (1- count) * 128;
    var top_px = 0;
    if (pos_px != total_pos_px){
        top_px = (pos_px - 128) + 'px';
        $('#banner_pic').css('top', top_px);
    } else {
        top_px = top_px + 'px';
        $('#banner_pic').css('top', top_px);
    }
}