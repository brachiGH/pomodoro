document.addEventListener('DOMContentLoaded', function() {
    var urlList = document.getElementById('url-list');
    var urlInput = document.getElementById('url-input');
    var addUrlButton = document.getElementById('add-url');
  
    addUrlButton.addEventListener('click', function() {
        var url = urlInput.value.trim();
        if (isValidUrl(url)) {
          var domainName = getDomainName(url);
          if (domainName) {
            browser.storage.local.get('urls').then(function(result) {
              var urls = result.urls || [];
              urls.push(domainName);
              browser.storage.local.set({ urls: urls }).then(function() {
                urlInput.value = '';
                displayUrls();
              });
            });
          }
        } else {
          alert('Invalid URL');
        }
      });
      
  
    function displayUrls() {
      urlList.innerHTML = '';
      browser.storage.local.get('urls').then(function(result) {
        var urls = result.urls || [];
        urls.forEach(function(url, index) {
          var li = document.createElement('li');
          li.textContent = url;
          
          // Add remove button
          var removeButton = document.createElement('button');
          removeButton.textContent = 'Remove';
          removeButton.addEventListener('click', function() {
            var url_ = urls.splice(index, 1);
            browser.storage.local.set({ urls: urls }).then(function() {
              displayUrls();
              browser.runtime.sendMessage({ action: 'updateTap', url: url_ });
            });
          });
          li.appendChild(removeButton);
          
          // Add change button
          var changeButton = document.createElement('button');
          changeButton.textContent = 'Change';
          changeButton.addEventListener('click', function() {
            var newUrl = prompt('Enter the new URL:', url);
            if (newUrl !== null) {
              urls[index] = newUrl.trim();
              browser.storage.local.set({ urls: urls }).then(function() {
                displayUrls();
                browser.runtime.sendMessage({ action: 'updateTap', url: newUrl.trim() });
              });
            }
          });
          li.appendChild(changeButton);
          
          urlList.appendChild(li);
        });
      });
    }
  
    displayUrls();
  });
  


  function isValidUrl(url) {
    try {
      new URL(url);
      return true;
    } catch (error) {
      return false;
    }
  }
  
  function getDomainName(url) {
    try {
      var parsedUrl = new URL(url);
      return parsedUrl.hostname;
    } catch (error) {
      return null;
    }
  }
  