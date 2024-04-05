chrome.tabs.onActivated.addListener(function (activeInfo) {
  chrome.tabs.get(activeInfo.tabId).then(checkTapRequest);
});

chrome.tabs.onCreated.addListener(function (tab) {
  checkTapRequest(tab);
});

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if (changeInfo.status === 'complete') {
    checkTapRequest(tab);
  }
});

function checkTapRequest(tab) {
  checkServerStatus().then(isActive => {
    checkTap(tab, isActive);
  });
}

function checkTap(tab, isTimerActive=false) {
  var url = tab.url;
  var tabId = tab.id;
  var domainName = getDomainName(url);
  if (domainName && isTimerActive) {
    chrome.storage.local.get('urls').then(function (result) {
      var urls = result.urls || [];
      if (urls.includes(domainName)) {
        chrome.tabs.sendMessage(tabId, { action: 'blockAccess' });
      }
    });
  } else {
    chrome.tabs.sendMessage(tabId, { action: 'unblockAccess' });
  }
}

chrome.runtime.onMessage.addListener(function (message, sender) {
  if (message.action === 'updateTap') {
    chrome.tabs.query({}).then(function (tabs) {
      checkServerStatus().then(isActive => {
        tabs.forEach(function (tab) {
          checkTap(tab,isActive);
        });
      });
    });
  }
});

function checkServerStatus() {
  return fetch('http://127.0.0.1:7847/isactive')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.text();
    })
    .then(data => {
      return data.trim() === 'active';
    })
    .catch(error => {
      console.error('Error:', error);
      return false;
    });
}



function getDomainName(url) {
  try {
    var parsedUrl = new URL(url);
    return parsedUrl.hostname;
  } catch (error) {
    return null;
  }
}