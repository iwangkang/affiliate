/* 公共函数库 */
$('#more_id').live('click', function(e) {
    e.stopPropagation();
    if (!($(this).hasClass('gbto'))){
        $(this).addClass('gbto');
        $('#gbd').attr('style', 'visibility: visible; right: auto; left: 0px;');
    } else {
        $(this).removeClass('gbto');
        $('#gbd').attr('style', 'visibility: hidden;');
    }

    $(window).click(function(){
        if ($('#more_id').hasClass('gbto')){
            $('#more_id').click();
        }
        $(this).unbind('click');
    });
});

//搜索热词推荐
$('#gbqfq').live('keyup', function(e){
    e.stopPropagation();
    var code = (e.keyCode ? e.keyCode : e.which);
    if (code == 38 || code == 40){
        //过滤判断是否是上线选项键
        check_up_and_down(e);
    } else {
        //ajax刷新推荐词列表
        if ($('#gbqfq').val()){
            refresh_hot_word_list();
        } else {
            $('#hot_word_list').empty();
        }
    }

    $(window).click(function(){
        $('#hot_word_list').empty()
        $(this).unbind('click');
    });
});

//搜索热词推荐
$('.hot_word').live('mouseover', function(){
    $('.hot_word').each(function(){
        if ($(this).hasClass('gssb_i')) {
            $(this).removeClass('gssb_i');
        }
    });
    $(this).addClass('gssb_i');
    var keyword = $(this).find('td', 0).find('div', 0).find('table', 0).find('tbody', 0).find('tr', 0).find('td', 0).find('span', 0).text();
    $('#gbqfq').val(keyword);
});

$('.hot_word').live('click', function(){
    $('#gbqfb').click();
});

function check_up_and_down(e){
    var code = (e.keyCode ? e.keyCode : e.which);
    var over_backgroud_flag = false;
    var keyword = '';
    if (code == 40) {
        $('.hot_word').each(function(){
            if ($(this).hasClass('gssb_i')){
                over_backgroud_flag = true;
                $(this).removeClass('gssb_i');
                if ($(this).next().hasClass('hot_word')){
                    $(this).next().addClass('gssb_i');
                    keyword = $(this).next().find('td', 0).find('div', 0).find('table', 0).find('tbody', 0).find('tr', 0).find('td', 0).find('span', 0).text();
                } else {
                    $('.hot_word').first().addClass('gssb_i');
                    keyword = $('.hot_word').first().find('td', 0).find('div', 0).find('table', 0).find('tbody', 0).find('tr', 0).find('td', 0).find('span', 0).text();
                }
                $('#gbqfq').val(keyword);
            }
            if (over_backgroud_flag) {
                return false;
            }
        });
    } else if (code == 38) {
        $('.hot_word').each(function(){
            if ($(this).hasClass('gssb_i')){
                over_backgroud_flag = true;
                $(this).removeClass('gssb_i');
                if ($(this).prev().hasClass('hot_word')){
                    $(this).prev().addClass('gssb_i');
                    keyword = $(this).prev().find('td', 0).find('div', 0).find('table', 0).find('tbody', 0).find('tr', 0).find('td', 0).find('span', 0).text();
                } else {
                    $('.hot_word').last().addClass('gssb_i');
                    keyword = $('.hot_word').last().find('td', 0).find('div', 0).find('table', 0).find('tbody', 0).find('tr', 0).find('td', 0).find('span', 0).text();
                }
                $('#gbqfq').val(keyword);
            }
            if (over_backgroud_flag) {
                return false;
            }
        });
    }
    if (!over_backgroud_flag){
        var keyword = '';
        if (code == 38) {
            $('.hot_word').last().addClass('gssb_i');
            keyword = $('.hot_word').last().find('td', 0).find('div', 0).find('table', 0).find('tbody', 0).find('tr', 0).find('td', 0).find('span', 0).text();
        } else if (code == 40) {
            $('.hot_word').first().addClass('gssb_i');
            keyword = $('.hot_word').first().find('td', 0).find('div', 0).find('table', 0).find('tbody', 0).find('tr', 0).find('td', 0).find('span', 0).text();
        }
        $('#gbqfq').val(keyword);
    }
}

function refresh_hot_word_list(){
    var keyword = $('#gbqfq').val();
    $.ajax({
        type: 'POST',
        url: '/hot_w',
        data: 'keyword=' + keyword,
        cache: true,
        dataType: 'json',
        success: function(data) {
            var content = '';
            $.each(data, function(i, element){
                content += '<tr class="hot_word">';
                content += '    <td style="text-align: left;" dir="ltr" class="gssb_a gbqfsf">';
                content += '        <div class="gsq_a">';
                content += '            <table style="width: 100%;" cellpadding="0" cellspacing="0">';
                content += '                <tbody>';
                content += '                    <tr>';
                content += '                        <td style="width: 100%;">';
                content += '                            <span>' + element + '</span>';
                content += '                        </td>';
                content += '                    </tr>';
                content += '                </tbody>';
                content += '            </table>';
                content += '        </div>';
                content += '    </td>';
                content += '</tr>';
            });
            $('#hot_word_list').empty().append(content);
        }
    });
}
