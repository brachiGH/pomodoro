browser.tabs.onActivated.addListener(function (activeInfo) {
  browser.tabs.get(activeInfo.tabId).then(checkTapRequest);
});

browser.tabs.onCreated.addListener(function (tab) {
  checkTapRequest(tab);
});

browser.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
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
    browser.storage.local.get('urls').then(function (result) {
      var urls = result.urls || [];
      if (urls.includes(domainName)) {
        browser.tabs.sendMessage(tabId, { action: 'blockAccess' });
      }
    });
  } else {
    browser.tabs.sendMessage(tabId, { action: 'unblockAccess' });
  }
}

browser.runtime.onMessage.addListener(function (message, sender) {
  if (message.action === 'updateTap') {
    browser.tabs.query({}).then(function (tabs) {
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