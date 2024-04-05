chrome.runtime.onMessage.addListener(function(message) {
    if (message.action === 'captureUrl') {
      var url = message.url;
      var domainName = getDomainName(url);
      if (domainName) {
        chrome.runtime.sendMessage({ action: 'checkUrl', domainName: domainName });
      }
    } else if (message.action === 'blockAccess') {
      showAccessDeniedMessage()
    } else if (message.action === 'unblockAccess') {
      removeAccessDeniedMessage()
    }
});
  
function getDomainName(url) {
    try {
        var parsedUrl = new URL(url);
        return parsedUrl.hostname;
    } catch (error) {
        return null;
    }
}

function showAccessDeniedMessage() {
  // Check if the message div already exists
  if (document.getElementById('access-denied-message')) {
    return; // If it exists, do nothing
  }

  // Create a div element for the message
  var messageDiv = document.createElement('div');
  messageDiv.id = 'access-denied-message';
  messageDiv.textContent = "Access Denied. You can't access this page now.";

  // Style the message div
  messageDiv.style.position = 'fixed';
  messageDiv.style.top = 0;
  messageDiv.style.left = 0;
  messageDiv.style.width = '100%';
  messageDiv.style.height = '100%';
  messageDiv.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
  messageDiv.style.color = '#fff';
  messageDiv.style.fontFamily = 'Arial, sans-serif';
  messageDiv.style.fontSize = '24px';
  messageDiv.style.display = 'flex';
  messageDiv.style.justifyContent = 'center';
  messageDiv.style.alignItems = 'center';
  messageDiv.style.zIndex = 9999999999;

  // Append the message div to the document body
  document.body.appendChild(messageDiv);

  // Disable key press events
  document.addEventListener('keydown', function(event) {
    event.preventDefault();
  });

  // Disable mouse scroll events
  document.addEventListener('wheel', function(event) {
    event.preventDefault();
  }, { passive: false });
}


function removeAccessDeniedMessage() {
  var messageDiv = document.getElementById('access-denied-message');
  if (messageDiv) {
    messageDiv.parentNode.removeChild(messageDiv);
  }
}