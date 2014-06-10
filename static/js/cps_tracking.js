/* cps tracking */
window.onload=c_o;
function xc_jsonp(url){
    var script_node = document.createElement('script');
    script_node.src = url;
    script_node.type = 'text/javascript';
    document.getElementsByTagName('html')[0].appendChild(script_node);
    script_node.remove();
}
function suc(res){}
function order(res){}
function c_o(){
    var url = 'http://api.affiliate.xingcloud.com/cps?callback=suc';
    xc_jsonp(url);
}
function xc_parser(str){
    str = str.replace('+', '%2B').replace('/', '%2F').replace('?', '%3F').replace('#', '%23').replace('&', '%26');
    return str;
}
function xc_listening(orderList){
    var orderListJson = JSON.stringify(orderList);
    var url = 'http://api.affiliate.xingcloud.com/cps?callback=order&orderList=' + xc_parser(orderListJson);
    xc_jsonp(url);
}