// QR Code Generator — core logic
// Depends on the global QRCode object (loaded via deferred <script> tag).
(function () {
  let currentTab = 'url';
  let qrCodeInstance = null;

  const qrContainer = document.getElementById('qrcode');
  const qrInput = document.getElementById('qr-input');
  const inputLabel = document.getElementById('input-label');
  const tabUrlBtn = document.getElementById('tab-url');
  const tabTextBtn = document.getElementById('tab-text');

  if (!qrContainer || !qrInput) {
    // Not on a page that has the generator UI; do nothing.
    return;
  }

  const ACTIVE_TAB_CLASS = 'px-6 py-2 text-sm font-medium rounded-md transition-all bg-white text-slate-900 shadow-sm';
  const INACTIVE_TAB_CLASS = 'px-6 py-2 text-sm font-medium rounded-md transition-all text-slate-600 hover:text-slate-900';

  function renderQRCode(text) {
    qrContainer.innerHTML = '';
    qrCodeInstance = new QRCode(qrContainer, {
      text: text,
      width: 160,
      height: 160,
      colorDark: '#000000',
      colorLight: '#ffffff',
      correctLevel: QRCode.CorrectLevel.H,
    });
  }

  function switchTab(tab) {
    currentTab = tab;

    if (tab === 'url') {
      tabUrlBtn.className = ACTIVE_TAB_CLASS;
      tabTextBtn.className = INACTIVE_TAB_CLASS;
      inputLabel.innerText = 'Destination URL';
      qrInput.value = 'https://example.com';
      qrInput.placeholder = 'https://example.com';
    } else {
      tabTextBtn.className = ACTIVE_TAB_CLASS;
      tabUrlBtn.className = INACTIVE_TAB_CLASS;
      inputLabel.innerText = 'Content Text';
      qrInput.value = 'Hello World';
      qrInput.placeholder = 'Enter text here';
    }

    generateQRCode();
  }

  function generateQRCode() {
    const val = qrInput.value.trim();
    if (!val) return;
    renderQRCode(val);
  }

  function downloadQRCode() {
    const img = qrContainer.querySelector('img');
    const canvas = qrContainer.querySelector('canvas');

    let imageSrc = '';
    if (img && img.src) {
      imageSrc = img.src;
    } else if (canvas) {
      imageSrc = canvas.toDataURL('image/png');
    }

    if (!imageSrc) return;

    const link = document.createElement('a');
    link.href = imageSrc;
    link.download = `qrcode-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // Expose the handlers the HTML's onclick attributes need.
  window.switchTab = switchTab;
  window.generateQRCode = generateQRCode;
  window.downloadQRCode = downloadQRCode;

  document.addEventListener('DOMContentLoaded', function () {
    renderQRCode(qrInput.value);
  });
})();
