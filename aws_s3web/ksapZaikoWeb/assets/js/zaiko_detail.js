url = "https://glb20se6vi.execute-api.ap-northeast-1.amazonaws.com/production/zaikoapi";
//url = "https://n2vcdsv6gd.execute-api.ap-northeast-1.amazonaws.com/APIseatstage/seatmotionresource";
var jsondata = "";

$(document).ready(function(){
    reloadZaiko();

    //3秒に1回着席情報を更新する
    setInterval(reloadZaiko,3000);
})

function reloadZaiko(){
    
    //APIGateWayにリクエスト
    $.ajax({
        dataType : "json",
        data : JSON.stringify(jsondata),
        type : "POST",
        url : url,
        success: function(data){
            //取得データ分ループする
            data.Items.forEach(function(item){

                zaikoPanel = $('#zaiko-' + item.id)[0]

                // 在庫が画面になければ追加
                if (zaikoPanel == null){
                    zaikoPanel = appendZaiko(item);
                }

                // 属性を設定
                zaikoPanel.getElementsByClassName('zaiko-name')[0].innerHTML = item.name;
                zaikoPanel.getElementsByClassName('zaiko-su')[0].innerHTML = item.zaikosu + " " + item.tani;
                zaikoPanel.getElementsByClassName('zaiko-weight')[0].innerHTML = item.weight + " g";
                zaikoPanel.getElementsByClassName('zaiko-weight-box')[0].innerHTML = "( 箱 " + item.weight_box + " g )";
                zaikoPanel.getElementsByClassName('zaiko-maker')[0].innerHTML = item.maker;
                zaikoPanel.getElementsByClassName('zaiko-yj')[0].innerHTML = item.yj_cd;
                zaikoPanel.getElementsByClassName('zaiko-yakka')[0].innerHTML = item.yakka + "円／" + item.tani;
                zaikoPanel.getElementsByClassName('zaiko-weight-one')[0].innerHTML = item.weight_one + " g／" + item.tani;
                zaikoPanel.getElementsByClassName('zaiko-img')[0].src = "./assets/img/" + item.id + ".jpeg";
            
            });
        }
    });
}

//zaiko-panelタグの作成
function appendZaiko(item){

    // スケルトンの取得
    const skeltonElement = $('#zaiko-skelton')[0];
    // コピーして新たに作成
    var newZaiko = skeltonElement.cloneNode(true);
    // id名設定
    newZaiko.id = "zaiko-" + item.id;
    // 追加
    $(".zaiko-view")[0].appendChild(newZaiko);
    // 追加した在庫を返却    
    return $('#zaiko-' + item.id)[0];
}
