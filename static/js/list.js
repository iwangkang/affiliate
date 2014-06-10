/* 列表页函数库 */
$(document).ready(function(){
    init_page_event();
    init_page_view();
    init_sort_view();
    init_filter_view();
});

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
    var page_index = parseInt($('#page_index').text());
    var page_count = parseInt($('#page_count').text());
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
$('#stt__ps-view').live('click', function(e){
    e.stopPropagation();
    var style = $('#list_web').attr('style');
    var show_style = 'z-index: 150; -moz-user-select: none; visibility: visible; left: 2px; top: 21px;';
    var hidden_style = 'z-index: 150; -moz-user-select: none; visibility: visible; left: 2px; top: 21px;display: none;';
    if (style == show_style) {
        $('#list_web').attr('style', hidden_style);
    } else {
        $('#list_web').attr('style', show_style);
    }

    $(window).click(function(){
        if (style == hidden_style){
            $('#stt__ps-view').click();
        }
        $(this).unbind('click');
    });
});

//排序样式控制
$('#stt__ps-sort').live('click', function(e){
    e.stopPropagation();
    if ($('#stt__ps-sort-m').hasClass('active')){
        $('#stt__ps-sort-m').removeClass('active');
        $('#stt__ps-sort-m').attr('style', 'display: none; z-index: 150;');
    } else {
        $('#stt__ps-sort-m').addClass('active');
        $('#stt__ps-sort-m').attr('style', 'z-index: 150;');
    }

    $(window).click(function(){
        if ($('#stt__ps-sort-m').hasClass('active')){
            $('#stt__ps-sort').click();
        }
        $(this).unbind('click');
    });
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

//列表页详情展示事件
$('.show_detail_list').live('click', function(){
    $('#show_detail_li').remove();
    $('.show_detail_list').each(function(){
        $(this).attr('style', '');
    });
    $(this).attr('style', 'display: none;');
    //获取参数
    var tilte = $(this).attr('p-title');
    var product_url = $(this).attr('p-url');
    var category = $(this).attr('p-category');
    var img = $(this).attr('p-img');
    var description = $(this).attr('p-desc');
    var currency = $(this).attr('p-currency');
    var price = $(this).attr('p-price');
    var publish_date = $(this).attr('p-publish');
    var merchant = $(this).attr('p-merchant');

    var content = "<li id=\"show_detail_li\" style=\"\" data-docid=\"1212882303229050520\" class=\"pspo-popout pspo-gpop\">";
    content += "<div jstcache=\"2\" class=\"pspo-desktop\">";
    content += "    <div class=\"pspo-container\">";
    content += "       <div class=\"pspo-sc\">";
    content += "            <a class=\"pspo-close\" id=\"close_detail_list_li\" href=\"javascript:void(0)\" jsaction=\"spop.x\"></a>";
    content += "            <div class=\"pspo-ic\" style=\"width: 300px\">";
    content += "                <div class=\"pspo-ilinks pspo-noiw\" style=\"width: 300px; height: 300px\">";
    content += "                    <a class=\"pspo-image\" href=\"" + product_url + "\">";
    content += "                        <div class=\"thumbnail-div\" style=\"width: 300px; height: 300px\">";
    content += "                            <img style=\"width: 300px; height: 300px;\" src=\"" + img + "\">";
    content += "                        </div>";
    content += "                    </a>";
    content += "                </div>";
    content += "            </div>";
    content += "            <div class=\"pspo-content\" style=\"margin-left: 335px; min-height: 300px\">";
    content += "                <a class=\"pspo-title\" href=\"" + product_url + "\">" + tilte + "</a>";
    content += "                <div class=\"f psae-pop\">";
    content += "                    <span>";
    content += "                        <span style=\"display: none\">&nbsp;·</span>";
    content += "                        <span style=\"display: none\"> ·&nbsp;</span>";
    content += "                        <span>";
    content += "                            <span class=\"psae-at\">Product</span>";
    content += "                        </span>";
    content += "                    </span>";
    content += "                    <span>";
    content += "                        <span>&nbsp;· </span>";
    content += "                        <span style=\"display: none\"> ·&nbsp;</span>";
    content += "                        <span>";
    content += "                            <span class=\"psae-at\">Description</span>";
    content += "                        </span>";
    content += "                    </span>";
    content += "                </div>";
    content += "                <p class=\"pspo-desc\">";
    content += "                    <span class=\"pspo-tdesc\">";
    content += "                        <span>" + description.substring(0, 59) + "...</span>";
    content += "                        <span>";
    content += "                            <a style=\"opacity: 1;\" class=\"pspo-fade pspo-togdesc flt simple_desc\" href=\"javascript:void(0)\" jsaction=\"spop.td\">More&nbsp;»</a>";
    content += "                        </span>";
    content += "                    </span>";
    content += "                    <span class=\"pspo-fdesc\" style=\"display: none\">";
    content += "                        <span>" + description + "</span>";
    content += "                        <a class=\"pspo-togdesc flt more_desc\" href=\"javascript:void(0)\" jsaction=\"spop.td\">«&nbsp;Show describe</a>";
    content += "                    </span>";
    content += "                </p>";
    content += "                <div style=\"display: none;\" class=\"pspo-hoffers pspo-unfade\">";
    content += "                    <div class=\"pspo-hoffer pspo-hofferwithalt\"></div>";
    content += "                    <div class=\"pspo-haltoffers\"></div>";
    content += "                    <div class=\"psclear\"></div>";
    content += "                </div>";
    content += "                <div style=\"opacity: 1;\" class=\"pspo-fade\">";
    content += "                    <div class=\"pspo-offers\">";
    content += "                        <div class=\"pspo-offer pspo-offerwithalt\">";
    content += "                            <a class=\"pspo-offer-link kpbb\" href=\"" + product_url + "\">";
    content += "                                <div class=\"pspo-ol-price pspo-ol-lprice\">" + currency + "&nbsp;" + price + "</div>";
    content += "                                <div class=\"pspo-ol-details\">";
    content += "                                    <div style=\"\" class=\"pspo-ol-seller\">" + category + "</div>";
    content += "                                    <div>Provided By：" + merchant + "</div>";
    content += "                                </div>";
    content += "                                <div class=\"psclear\"></div>";
    content += "                            </a>";
    content += "                            <div class=\"pspo-offer-flare\">";
    content += "                                <span>";
    content += "                                    <span class=\"shoppingstarsjs__stars\" style=\"background-image: url(/static/images/page/shopping_sprites186_hr.png); background-position: -17px 0px; height: 13px; width: 65px; background-size: 128px\">";
    content += "                                        <span class=\"shoppingstarsjs__stars\" aria-label=\"4.5\" role=\"img\" style=\"background-image: url(/static/images/page/shopping_sprites186_hr.png); height: 13px; width: 58px; background-size: 128px; background-position: -17px -14px\"></span>";
    content += "                                    </span>";
    content += "                                </span>";
    content += "                            </div>";
    content += "                        </div>";
    content += "                        <div class=\"pspo-altoffers\">";
    content += "                            <table class=\"pspo-altot\">";
    content += "                                <tbody>";
    content += "                                    <tr class=\"pspo-altoffer\">";
    content += "                                        <td class=\"pspo-altprice\">" + currency + "&nbsp;" + price + "</td>";
    content += "                                        <td class=\"pspo-altofferlink\">";
    content += "                                            <a>" + category + "</a>";
    content += "                                        </td>";
    content += "                                    </tr>";
    content += "                                </tbody>";
    content += "                            </table>";
    content += "                            <strong>Published Date：</strong>" + publish_date;
    content += "                        </div>";
    content += "                        <div class=\"psclear\"></div>";
    content += "                    </div>";
    content += "                    <div class=\"psclear\"></div>";
    content += "                    <div class=\"pspo-bottom\">";
    content += "                        <div class=\"pspo-shortlist\"></div>";
//    content += "                        <div style=\"opacity: 1;\" class=\"pspo-pp-sections pspo-fade\">";
//    content += "                            <a class=\"pspo-pp-section\" href=\"\">Related products</a>";
//    content += "                        </div>";
    content += "                        <div class=\"psclear\"></div>";
    content += "                    </div>";
    content += "                    <div class=\"psclear\"></div>";
    content += "                    <div class=\"pspo-buffer\"></div>";
    content += "                    <div style=\"display: none\">";
    content += "                        <div class=\"pspo-vs__section\">";
    content += "                            <div class=\"pspo-vs__title\">Similar in appearance to the product</div>";
    content += "                            <div class=\"pspo-vs__psclear\"></div>";
    content += "                            <div class=\"pspo-vs__buffer\"></div>";
    content += "                            <div class=\"pspo-vs__resultgroup\">";
    content += "                                <a class=\"pspo-vs__more-link\" href=\"#\">more</a>";
    content += "                            </div>";
    content += "                        </div>";
    content += "                    </div>";
    content += "                </div>";
    content += "                <div class=\"psclear\"></div>";
    content += "            </div>";
    content += "        </div>";
    content += "    </div>";
    content += "</div>";
    content += "</li>";

    $(this).after(content);
//    $('#show_detail_li').slideDown(900);
});

$('.show_detail').live('click', function(){
    $('#show_detail_li').remove();
    $('.show_detail').each(function(){
        if ($(this).hasClass('active')){
            $(this).removeClass('active');
        }
    });
    $(this).addClass('active');
    //获取参数
    var tilte = $(this).attr('p-title');
    var product_url = $(this).attr('p-url');
    var category = $(this).attr('p-category');
    var img = $(this).attr('p-img');
    var description = $(this).attr('p-desc');
    var currency = $(this).attr('p-currency');
    var price = $(this).attr('p-price');
    var publish_date = $(this).attr('p-publish');
    var merchant = $(this).attr('p-merchant');
    //计算偏移量
    var line_no = $(this).attr('line-no');
    var product_total_count = $('.show_detail').length;
    var product_no = $(this).attr('p-no');
    if ((product_total_count - product_no) >= 6){
        var interval_count = 6 - line_no;
        var arrows_px = 'left: ' + (85 + 191 * (line_no-1)) + 'px;';
    } else {
        var interval_count = product_total_count - product_no;
        var arrows_px = 'left: ' + (85 + 191 * (line_no-1)) + 'px;';
    }

    var content = "<li id=\"show_detail_li\" style=\"display: none;\" data-docid=\"1212882303229050520\" class=\"pspo-popout pspo-gpop\">";
    content += "<div jstcache=\"2\" class=\"pspo-desktop\">";
    content += "    <div style=\"" + arrows_px + "\" class=\"pspo-arrow\"></div>";
    content += "    <div class=\"pspo-container\">";
    content += "       <div class=\"pspo-sc\">";
    content += "            <a class=\"pspo-close\" id=\"close_detail_li\" href=\"javascript:void(0)\" jsaction=\"spop.x\"></a>";
    content += "            <div class=\"pspo-ic\" style=\"width: 300px\">";
    content += "                <div class=\"pspo-ilinks pspo-noiw\" style=\"width: 300px; height: 300px\">";
    content += "                    <a target=\"_blank\" class=\"pspo-image\" href=\"" + product_url + "\">";
    content += "                        <div class=\"thumbnail-div\" style=\"width: 300px; height: 300px\">";
    content += "                            <img style=\"width: 300px; height: 300px;\" src=\"" + img + "\">";
    content += "                        </div>";
    content += "                    </a>";
    content += "                </div>";
    content += "            </div>";
    content += "            <div class=\"pspo-content\" style=\"margin-left: 335px; min-height: 300px\">";
    content += "                <a target=\"_blank\" class=\"pspo-title\" href=\"" + product_url + "\">" + tilte + "</a>";
    content += "                <div class=\"f psae-pop\">";
    content += "                    <span>";
    content += "                        <span style=\"display: none\">&nbsp;·</span>";
    content += "                        <span style=\"display: none\"> ·&nbsp;</span>";
    content += "                        <span>";
    content += "                            <span class=\"psae-at\">Product</span>";
    content += "                        </span>";
    content += "                    </span>";
    content += "                    <span>";
    content += "                        <span>&nbsp;· </span>";
    content += "                        <span style=\"display: none\"> ·&nbsp;</span>";
    content += "                        <span>";
    content += "                            <span class=\"psae-at\">Description</span>";
    content += "                        </span>";
    content += "                    </span>";
    content += "                </div>";
    content += "                <p class=\"pspo-desc\">";
    content += "                    <span class=\"pspo-tdesc\">";
    content += "                        <span>" + description.substring(0, 59) + "...</span>";
    content += "                        <span>";
    content += "                            <a style=\"opacity: 1;\" class=\"pspo-fade pspo-togdesc flt simple_desc\" href=\"javascript:void(0)\" jsaction=\"spop.td\">More&nbsp;»</a>";
    content += "                        </span>";
    content += "                    </span>";
    content += "                    <span class=\"pspo-fdesc\" style=\"display: none\">";
    content += "                        <span>" + description + "</span>";
    content += "                        <a class=\"pspo-togdesc flt more_desc\" href=\"javascript:void(0)\" jsaction=\"spop.td\">«&nbsp;Show brief</a>";
    content += "                    </span>";
    content += "                </p>";
    content += "                <div style=\"display: none;\" class=\"pspo-hoffers pspo-unfade\">";
    content += "                    <div class=\"pspo-hoffer pspo-hofferwithalt\"></div>";
    content += "                    <div class=\"pspo-haltoffers\"></div>";
    content += "                    <div class=\"psclear\"></div>";
    content += "                </div>";
    content += "                <div style=\"opacity: 1;\" class=\"pspo-fade\">";
    content += "                    <div class=\"pspo-offers\">";
    content += "                        <div class=\"pspo-offer pspo-offerwithalt\">";
    content += "                            <a target=\"_blank\" class=\"pspo-offer-link kpbb\" href=\"" + product_url + "\">";
    content += "                                <div class=\"pspo-ol-price pspo-ol-lprice\">" + currency + "&nbsp;" + price + "</div>";
    content += "                                <div class=\"pspo-ol-details\">";
    content += "                                    <div style=\"\" class=\"pspo-ol-seller\">" + category + "</div>";
    content += "                                    <div>Provided By：" + merchant + "</div>";
    content += "                                </div>";
    content += "                                <div class=\"psclear\"></div>";
    content += "                            </a>";
    content += "                            <div class=\"pspo-offer-flare\">";
    content += "                                <span>";
    content += "                                    <span class=\"shoppingstarsjs__stars\" style=\"background-image: url(/static/images/page/shopping_sprites186_hr.png); background-position: -17px 0px; height: 13px; width: 65px; background-size: 128px\">";
    content += "                                        <span class=\"shoppingstarsjs__stars\" aria-label=\"4.5\" role=\"img\" style=\"background-image: url(/static/images/page/shopping_sprites186_hr.png); height: 13px; width: 58px; background-size: 128px; background-position: -17px -14px\"></span>";
    content += "                                    </span>";
    content += "                                </span>";
    content += "                            </div>";
    content += "                        </div>";
    content += "                        <div class=\"pspo-altoffers\">";
    content += "                            <table class=\"pspo-altot\">";
    content += "                                <tbody>";
    content += "                                    <tr class=\"pspo-altoffer\">";
    content += "                                        <td class=\"pspo-altprice\">" + currency + "&nbsp;" + price + "</td>";
    content += "                                        <td class=\"pspo-altofferlink\">";
    content += "                                            <a>" + category + "</a>";
    content += "                                        </td>";
    content += "                                    </tr>";
    content += "                                </tbody>";
    content += "                            </table>";
    content += "                            <strong>Published Date：</strong>" + publish_date;
    content += "                        </div>";
    content += "                        <div class=\"psclear\"></div>";
    content += "                    </div>";
    content += "                    <div class=\"psclear\"></div>";
    content += "                    <div class=\"pspo-bottom\">";
    content += "                        <div class=\"pspo-shortlist\"></div>";
//    content += "                        <div style=\"opacity: 1;\" class=\"pspo-pp-sections pspo-fade\">";
//    content += "                            <a class=\"pspo-pp-section\" href=\"\">Related products</a>";
//    content += "                        </div>";
    content += "                        <div class=\"psclear\"></div>";
    content += "                    </div>";
    content += "                    <div class=\"psclear\"></div>";
    content += "                    <div class=\"pspo-buffer\"></div>";
    content += "                    <div style=\"display: none\">";
    content += "                        <div class=\"pspo-vs__section\">";
    content += "                            <div class=\"pspo-vs__title\">Similar in appearance to the product</div>";
    content += "                            <div class=\"pspo-vs__psclear\"></div>";
    content += "                            <div class=\"pspo-vs__buffer\"></div>";
    content += "                            <div class=\"pspo-vs__resultgroup\">";
    content += "                                <a target=\"_blank\" class=\"pspo-vs__more-link\" href=\"#\">More</a>";
    content += "                            </div>";
    content += "                        </div>";
    content += "                    </div>";
    content += "                </div>";
    content += "                <div class=\"psclear\"></div>";
    content += "            </div>";
    content += "        </div>";
    content += "    </div>";
    content += "</div>";
    content += "</li>";

    switch (interval_count){
        case 0:
            $(this).after(content);
            break;
        case 1:
            $(this).next().after(content);
            break;
        case 2:
            $(this).next().next().after(content);
            break;
        case 3:
            $(this).next().next().next().after(content);
            break;
        case 4:
            $(this).next().next().next().next().after(content);
            break;
        case 5:
            $(this).next().next().next().next().next().after(content);
            break;
    }

    $('#show_detail_li').slideDown(900);
    middle_show();
});

//产品详情居中
function middle_show(){
    //获取可视区高度
    var view_height = document.documentElement.clientHeight;
    //获取节点到浏览器顶端的距离
    var browser_top = document.getElementById('show_detail_li').getBoundingClientRect().bottom;
    //滚动条滚动距离
    var roll_distance = Math.max((document.body?document.body.scrollTop:0), (document.documentElement?document.documentElement.scrollTop:0));
    var roll_y = (browser_top - view_height/ 3) + roll_distance;
    window.scrollTo(0, roll_y);
}

$('#close_detail_list_li').live('click', function(){
    $('.show_detail_list').each(function(){
        $(this).attr('style', '');
    });
    $('#show_detail_li').remove();
});

$('#close_detail_li').live('click', function(){
    $('.show_detail').each(function(){
        if ($(this).hasClass('active')){
            $(this).removeClass('active');
        }
    });
    $('#show_detail_li').slideUp(600);
});

//商品描述详情与简介切换事件
$('.simple_desc').live('click', function(){
    $(this).parent().parent().next().attr('style', '');
    $(this).parent().parent().attr('style', 'display: none;');
});

$('.more_desc').live('click', function(){
    $(this).parent().prev().attr('style', '');
    $(this).parent().attr('style', 'display: none;');
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
