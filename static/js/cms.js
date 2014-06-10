/* cms函数库 */
function getParam(){
    var begin = $('#begin').val();
    var end = $('#end').val();
    $.ajax({
        type: "POST",
        url: "/analysis?begin=" + begin + '&end=' + end,
        cache: true,
        dataType: "json",
        success: function(data) {
            g = new Dygraph(
                    document.getElementById("drawing"),
                    function () {
                        var r = "date,CPC,CPS\n";
                        $.each(data, function(i, element){
                            r += element + "\n";
                        })
                        return r;
                    },
                    {
                        labelsDiv: document.getElementById('status'),
                        labelsSeparateLines: true,
                        labelsKMB: false,
                        legend: 'always',
                        colors: ["rgb(51,204,204)",
                            "rgb(255,100,100)",
                            "#00DD55",
                            "rgba(50,50,200,0.4)"],
                        width: 640,
                        height: 480,
                        title: 'XingCloud CPC/CPS Shapes',
                        xlabel: 'Date',
                        ylabel: 'Count',
                        axisLineColor: 'white'
                        // drawXGrid: false
                    }
            );
        }
    });
}