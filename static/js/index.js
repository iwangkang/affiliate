/* 首页轮换 及 推荐产品翻页 */
$(document).ready(function(){
	window.setInterval(banner_timer, 6000);
});

// banner计时轮询器
function banner_timer(){
    var current_banner = $('.GGJHBMRCEG');
    var index = current_banner.attr('index');
    if (index != 3){
        current_banner.removeClass('GGJHBMRCEG');
        current_banner.next().addClass('GGJHBMRCEG');
        index = current_banner.next().attr('index');
        var top_px = '-' + (450 * parseInt(index)) + 'px';
        $('#banner_pic').css('top', top_px);
    } else {
        current_banner.removeClass('GGJHBMRCEG');
        $('#banner_first').addClass('GGJHBMRCEG');
        $('#banner_pic').css('top', '0px');
    }
}

// 鼠标移上事件
$('.banner').live('mouseover', function(){
    $('.GGJHBMRCEG').removeClass('GGJHBMRCEG');
    $(this).addClass('GGJHBMRCEG');
    var index = $(this).attr('index');
    var top_px = '-' + (450 * parseInt(index)) + 'px';
    $('#banner_pic').css('top', top_px);
});

// 新品推荐下一页
$('#next_new_page').live('click', function(){
    $(this).addClass('GGJHBMRCFD');
    $('#prev_new_page').removeClass('GGJHBMRCFD');
    $('#new_list').css('left', '-1020px');
    $('#new_page_no').text('item 7-12, 12 items total');
});

// 新品推荐上一页
$('#prev_new_page').live('click', function(){
    $(this).addClass('GGJHBMRCFD');
    $('#next_new_page').removeClass('GGJHBMRCFD');
    $('#new_list').css('left', '0px');
    $('#new_page_no').text('item 1-6, 12 items total');
});

// 热卖推荐下一页
$('#next_hot_page').live('click', function(){
    $(this).addClass('GGJHBMRCFD');
    $('#prev_hot_page').removeClass('GGJHBMRCFD');
    $('#hot_list').css('left', '-1020px');
    $('#hot_page_no').text('item 7-12, 12 items total');
});

// 新品推荐上一页
$('#prev_hot_page').live('click', function(){
    $(this).addClass('GGJHBMRCFD');
    $('#next_hot_page').removeClass('GGJHBMRCFD');
    $('#hot_list').css('left', '0px');
    $('#hot_page_no').text('item 1-6, 12 items total');
});