document.getElementById("changeColor")?.addEventListener("click", () => {
  screenShot()
})

function screenShot(){
  chrome.tabs.captureVisibleTab({ format: 'png' }, function (imageData) {
    //データ表示（バイナリ形式）
    save(imageData)
    console.log(imageData)
  });
}

function save(image: any){
  const data = image.split(',')[1]; // 'data:image/png;base64,' を除去
  const binaryData = atob(data); // Base64をデコード

  const byteArray = new Uint8Array(binaryData.length);
  for (let i = 0; i < binaryData.length; i++) {
    byteArray[i] = binaryData.charCodeAt(i);
  }
  const blob = new Blob([byteArray], { type: 'image/png' });

  // ダウンロード用URLを作成
  const url = URL.createObjectURL(blob);

  // `chrome.downloads.download` を使って画像を保存
  chrome.downloads.download({
    url: url,
    filename: 'screenshot.png',
  }, function(downloadId) {
    if (chrome.runtime.lastError) {
      console.error('画像の保存に失敗しました:', chrome.runtime.lastError);
    } else {
      console.log('画像のダウンロードが開始されました:', downloadId);
    }
  })
}