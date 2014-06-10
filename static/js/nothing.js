/* 列表页函数库 */
$(document).ready(function(){
    $('#foot').hide();
    init_suggest_link();
    init_page_event();
    init_page_view();
    init_sort_view();
    init_filter_view();
});

//初始化相关词链接
function init_suggest_link(){
    //参数获取
    var ck = $('#prev_page').attr('ck');
    var page_index = $('#page_index').text();
    var page_count = $('#page_count').text();
    var list_type = $('#stt__selected-view-item').attr('list-type');
    var price_sort = $('#stt__ps-sort').attr('sort-type');
    var check_status_dom = $('#new-product-view').find('span', 0);
    if (check_status_dom.hasClass('checked')){
        var filter_new = 'checked';
    } else {
        var filter_new = 'unchecked';
    }
    var lower_price = $('#lower_price').val();
    var upper_price = $('#upper_price').val();
    var merchant_name = $('#merchant_list').attr('merchant-name');
    var suggest_keyword = $('#suggest_keyword').find('em', 0).text();

    var suggest_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=' + filter_new + '&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + suggest_keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
    $('#suggest_keyword').attr('href', suggest_link);
}

//价格筛选
function fill_action(){
    //参数获取
    var keyword = $('#gbqfq').attr('keyword');
    var ck = $('#prev_page').attr('ck');
    var page_index = $('#page_index').text();
    var page_count = $('#page_count').text();
    var list_type = $('#stt__selected-view-item').attr('list-type');
    var price_sort = $('#stt__ps-sort').attr('sort-type');
    var check_status_dom = $('#new-product-view').find('span', 0);
    if (check_status_dom.hasClass('checked')){
        var filter_new = 'checked';
    } else {
        var filter_new = 'unchecked';
    }
    var lower_price = $('#lower_price').val();
    var upper_price = $('#upper_price').val();
    var merchant_name = $('#merchant_list').attr('merchant-name');

    var action_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=' + filter_new + '&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
    $('#filter_price_form').attr('action', action_link);
}

function init_filter_view(){
    //参数获取
    var keyword = $('#gbqfq').attr('keyword');
    var ck = $('#prev_page').attr('ck');
    var page_index = $('#page_index').text();
    var page_count = $('#page_count').text();
    var list_type = $('#stt__selected-view-item').attr('list-type');
    var price_sort = $('#stt__ps-sort').attr('sort-type');
    var lower_price = $('#lower_price').val();
    var upper_price = $('#upper_price').val();
    var merchant_name = $('#merchant_list').attr('merchant-name');

    var check_status_dom = $('#new-product-view').find('span', 0);
    if (check_status_dom.hasClass('checked')){
        var link_href = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=unchecked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
        var price_link_1 =  '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=checked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=&u_p=600';
        var price_link_2 =  '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=checked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=600&u_p=1000';
        var price_link_3 =  '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=checked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=1000&u_p=';
        var clear_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=checked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=1&pageSize=36&keyword=' + keyword + '&l_p=&u_p=';
        $('#new-product-view').attr('href', link_href);
        $('#less_then_600').attr('href', price_link_1);
        $('#600_to_1000').attr('href', price_link_2);
        $('#more_then_1000').attr('href', price_link_3);
        $('#clear_price_filter').attr('href', clear_link);
        $('#go_back_filter').attr('href', clear_link);
        $('.merchant_link').each(function(){
            var merchant_name = $(this).find('span', 1).text();
            if ($(this).find('span', 0).hasClass('checked')){
                var merchant_link = '/list?c_k=' + ck + '&m_n=&p_s=default&f_n=checked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
            } else {
                var merchant_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=checked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
            }
            $(this).attr('href', merchant_link);
        });
    } else {
        var link_href = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=checked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
        var price_link_1 =  '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=unchecked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=&u_p=600';
        var price_link_2 =  '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=unchecked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=600&u_p=1000';
        var price_link_3 =  '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=unchecked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=1000&u_p=';
        var clear_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=unchecked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=1&pageSize=36&keyword=' + keyword + '&l_p=&u_p=';
        $('#new-product-view').attr('href', link_href);
        $('#less_then_600').attr('href', price_link_1);
        $('#600_to_1000').attr('href', price_link_2);
        $('#more_then_1000').attr('href', price_link_3);
        $('#clear_price_filter').attr('href', clear_link);
        $('#go_back_filter').attr('href', clear_link);
        $('.merchant_link').each(function(){
            var merchant_name = $(this).find('span', 1).text();
            if ($(this).find('span', 0).hasClass('checked')){
                var merchant_link = '/list?c_k=' + ck + '&m_n=&p_s=default&f_n=unchecked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
            } else {
                var merchant_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=unchecked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
            }
            $(this).attr('href', merchant_link);
        });
    }
    var clear_filter_link = '/list?c_k=' + ck + '&m_n=&p_s=default&f_n=unchecked&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=1&pageSize=36&keyword=' + keyword + '&l_p=&u_p=';
    $('#clear_all_filter').attr('href', clear_filter_link);
}

//排序事件
function init_sort_view(){
    var keyword = $('#gbqfq').attr('keyword');
    var ck = $('#prev_page').attr('ck');
    var page_index = $('#page_index').text();
    var page_count = $('#page_count').text();
    var list_type = $('#stt__selected-view-item').attr('list-type');
    var check_status_dom = $('#new-product-view').find('span', 0);
    if (check_status_dom.hasClass('checked')){
        var filter_new = 'checked';
    } else {
        var filter_new = 'unchecked';
    }
    var lower_price = $('#lower_price').val();
    var upper_price = $('#upper_price').val();
    var merchant_name = $('#merchant_list').attr('merchant-name');

    var default_sort_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=default&f_n=' + filter_new + '&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
    var price_up_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=up&f_n=' + filter_new + '&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
    var price_down_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=down&f_n=' + filter_new + '&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
    $('#sort-view-default').attr('link-href', default_sort_link);
    $('#sort-view-price-up').attr('link-href', price_up_link);
    $('#sort-view-price-down').attr('link-href', price_down_link);
}

$('.sort-view').live('click', function(){
    var link_href = $(this).attr('link-href');
    window.location.href = link_href;
});

//分页事件
function init_page_view(){
    var keyword = $('#gbqfq').attr('keyword');
    var ck = $('#prev_page').attr('ck');
    var page_index = $('#page_index').text();
    var page_count = $('#page_count').text();
    var price_sort = $('#stt__ps-sort').attr('sort-type');
    var check_status_dom = $('#new-product-view').find('span', 0);
    if (check_status_dom.hasClass('checked')){
        var filter_new = 'checked';
    } else {
        var filter_new = 'unchecked';
    }
    var lower_price = $('#lower_price').val();
    var upper_price = $('#upper_price').val();
    var merchant_name = $('#merchant_list').attr('merchant-name');

    var web_view_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=' + price_sort + '&f_n=' + filter_new + '&l_t=w_v&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
    var list_view_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=' + price_sort + '&f_n=' + filter_new + '&l_t=l_v&webmaster=xc_shopping&pageIndex=' + parseInt(page_index) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
    $('#web-view').attr('link-href', web_view_link);
    $('#list-view').attr('link-href', list_view_link);
}

$('.list-view').live('click', function(){
    var link_href = $(this).attr('link-href');
    window.location.href = link_href;
});

function init_page_event(){
    var page_index = $('#page_index').text();
    var page_count = $('#page_count').text();
    var list_type = $('#stt__selected-view-item').attr('list-type');
    if (page_index == 1 & page_count == 1){
        $('#prev_page').addClass('GGJHBMRCFD');
        $('#next_page').addClass('GGJHBMRCFD');
    }else if (page_index == 1 & page_count > 1){
        $('#prev_page').addClass('GGJHBMRCFD');
        $('#next_page').removeClass('GGJHBMRCFD');
    } else if (page_index > 1 & page_index < page_count) {
        $('#prev_page').removeClass('GGJHBMRCFD');
        $('#next_page').removeClass('GGJHBMRCFD');
    } else if(page_index > 1 & page_index == page_count) {
        $('#prev_page').removeClass('GGJHBMRCFD');
        $('#next_page').addClass('GGJHBMRCFD');
    }
    var keyword = $('#gbqfq').attr('keyword');
    var ck = $('#prev_page').attr('ck');
    var price_sort = $('#stt__ps-sort').attr('sort-type');
    var check_status_dom = $('#new-product-view').find('span', 0);
    if (check_status_dom.hasClass('checked')){
        var filter_new = 'checked';
    } else {
        var filter_new = 'unchecked';
    }
    var lower_price = $('#lower_price').val();
    var upper_price = $('#upper_price').val();
    var merchant_name = $('#merchant_list').attr('merchant-name');

    var next_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=' + price_sort + '&f_n=' + filter_new + '&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + (parseInt(page_index) + 1) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
    var prev_link = '/list?c_k=' + ck + '&m_n=' + merchant_name + '&p_s=' + price_sort + '&f_n=' + filter_new + '&l_t=' + list_type + '&webmaster=xc_shopping&pageIndex=' + (parseInt(page_index) - 1) + '&pageSize=36&keyword=' + keyword + '&l_p=' + lower_price + '&u_p=' + upper_price;
    $('#next_page').attr('href', next_link);
    $('#prev_page').attr('href', prev_link);
}

//视图事件定义
$('#stt__ps-view').live('click', function(){
    var style = $('#list_web').attr('style');
    var show_style = 'z-index: 150; -moz-user-select: none; visibility: visible; left: 2px; top: 21px;';
    var hidden_style = 'z-index: 150; -moz-user-select: none; visibility: visible; left: 2px; top: 21px;display: none;';
    if (style == show_style) {
        $('#list_web').attr('style', hidden_style);
    } else {
        $('#list_web').attr('style', show_style);
    }
});

//排序样式控制
$('#stt__ps-sort').live('click', function(){
    if ($('#stt__ps-sort-m').hasClass('active')){
        $('#stt__ps-sort-m').removeClass('active');
        $('#stt__ps-sort-m').attr('style', 'display: none; z-index: 150;');
    } else {
        $('#stt__ps-sort-m').addClass('active');
        $('#stt__ps-sort-m').attr('style', 'z-index: 150;');
    }
});

//默认排序样式控制
$('#sort-view-default').live('mouseover', function(){
    $(this).attr('style', 'background-color: #eee;');
    $('#sort-view-price-up').attr('style', '');
    $('#sort-view-price-down').attr('style', '');
});

//按照价格升序排序样式控制
$('#sort-view-price-up').live('mouseover', function(){
    $(this).attr('style', 'background-color: #eee;');
    $('#sort-view-default').attr('style', '');
    $('#sort-view-price-down').attr('style', '');
});

//按照价格降序排序样式控制
$('#sort-view-price-down').live('mouseover', function(){
    $(this).attr('style', 'background-color: #eee;');
    $('#sort-view-price-up').attr('style', '');
    $('#sort-view-default').attr('style', '');
});

//网格视图样式控制
$('#web-view').live('mouseover', function(){
    $(this).attr('style', 'background-color: #eee;');
    $('#list-view').attr('style', '');
});

//列表视图样式控制
$('#list-view').live('mouseover', function(){
    $(this).attr('style', 'background-color: #eee;');
    $('#web-view').attr('style', '');
});

//商户筛选事件
$('#more_merchant').live('click', function(){
    $('#hidden_merchant').parent().attr('style', '');
    $(this).attr('style', 'display: none');
});

$('#hidden_merchant').live('click', function(){
    $(this).parent().attr('style', 'display: none');
    $('#more_merchant').attr('style', '');
});