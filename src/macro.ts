chrome.runtime.onInstalled.addListener(() => {
  console.log("TypeScript Extension installed!");
})


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'start') {
    console.log(message)
  }
  sendResponse({ success: true })
  return true
})