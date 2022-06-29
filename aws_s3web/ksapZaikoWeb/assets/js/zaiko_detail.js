url = "https://glb20se6vi.execute-api.ap-northeast-1.amazonaws.com/production/zaikoapi";

$(document).ready(function(){
    reloadZaiko();

    //3秒に1回着席情報を更新する
    setInterval(reloadZaiko,3000);
})

function reloadZaiko(){
    
    $('.zaiko-su').each(function(){
        $(this).removeClass("zaiko-su-blink")
    })

    //在庫個数情報の取得
    $.ajax({
        dataType : "json",
        data : JSON.stringify({"data-type":"zaiko-master"}),
        type : "POST",
        contentType: 'application/json',
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

    //払出情報の取得
    $.ajax({
        dataType : "json",
        data : JSON.stringify({"data-type":"zaiko-harai"}),
        type : "POST",
        contentType: 'application/json',
        url : url,
        success: function(data){
            // コンソールをクリアする
            clearHarai()
            //取得データ分ループする
            var idx = 1
            data.Items.forEach(function(item){
                // 在庫が画面になければ追加
                haraiRow = appendHarai(item ,idx++);
                // 属性を設定
                msg = (item.haraisu > 0 ? "払い出されました。" : "入庫されました。" )
                ts = item.datetime.replace("Z","")
                ts = new Date(Date.parse(ts))
                msg = "> " + 
                      ts.getMonth() + "月" + 
                      ts.getDate() + "日" + 
                      ts.getHours() + "時 " + 
                      ts.getMinutes() + "分" + 
                      ts.getSeconds() + "秒 " +
                      "「" + item.name + "」が " + 
                      Math.abs(item.haraisu) + "個 " + msg                
                haraiRow.innerHTML = msg

                // 在庫ラベルを点滅
                zaikoPanel = $('#zaiko-' + item.id)[0]
                zaikoPanel.getElementsByClassName('zaiko-su')[0].classList.add("zaiko-su-blink")
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

function clearHarai(){
    const haraiElements = $('.harai-row');
    for (raw in haraiElements){
        if (haraiElements[raw].id != 'harai-skelton') {
            $("#" + haraiElements[raw].id).remove()
        }
    }
}

//zaiko-panelタグの作成
function appendHarai(item,idx){

    // スケルトンの取得
    const skeltonElement = $('#harai-skelton')[0];
    // コピーして新たに作成
    var newHarai = skeltonElement.cloneNode(true);
    // id名設定
    newHarai.id = "harai-" + idx;
    // 追加
    $(".harai-area")[0].appendChild(newHarai);
    // 追加した在庫を返却    
    return $('#harai-' + idx)[0];
}
