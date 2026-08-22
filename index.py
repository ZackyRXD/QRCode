from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyFreeGenerator - QR Code Generator</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- QRCode.js Library (Client-side rendering) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <style>
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }
    </style>
</head>
<body class="bg-[#f4f5f7] min-h-screen text-slate-800 flex flex-col">

    <!-- Header Navigation -->
    <header class="w-full bg-white border-b border-gray-200 py-4 px-8 flex justify-between items-center">
        <h1 class="text-xl font-bold tracking-tight text-slate-900">MyFreeGenerator</h1>
        <button class="bg-[#1e2530] text-white px-5 py-2.5 rounded-md text-sm font-medium hover:bg-slate-800 transition-colors">
            Get Started
        </button>
    </header>

    <!-- Main Content Container -->
    <main class="flex-1 flex flex-col items-center justify-center px-4 py-12">
        
        <!-- Hero Title Section -->
        <div class="text-center max-w-2xl mb-10">
            <h2 class="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl mb-4">
                Generate QR Codes Instantly
            </h2>
            <p class="text-gray-500 text-lg leading-relaxed">
                Create crisp, high-resolution QR codes for links, text, or vCards with unmatched precision.
            </p>
        </div>

        <!-- Main Card Container -->
        <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-8 w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
            
            <!-- Left Input Form Area -->
            <div class="space-y-6">
                <!-- Tab Selector -->
                <div class="inline-flex p-1 bg-gray-100 rounded-lg">
                    <button id="tab-url" onclick="setTab('URL')" class="px-5 py-1.5 text-sm font-semibold rounded-md bg-white text-slate-900 shadow-sm transition-all">
                        URL
                    </button>
                    <button id="tab-text" onclick="setTab('Text')" class="px-5 py-1.5 text-sm font-medium text-gray-500 rounded-md hover:text-slate-900 transition-all">
                        Text
                    </button>
                </div>

                <!-- Input Field -->
                <div>
                    <label id="input-label" class="block text-sm font-medium text-gray-700 mb-2">
                        Destination URL
                    </label>
                    <input 
                        type="text" 
                        id="qr-input" 
                        placeholder="https://example.com" 
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-slate-800 focus:border-slate-800 outline-none transition-all text-slate-800 placeholder-gray-400"
                    />
                </div>

                <!-- Generate Button -->
                <button 
                    onclick="generateQRCode()" 
                    class="w-full bg-[#1e2530] hover:bg-slate-800 text-white font-semibold py-3.5 px-4 rounded-lg transition-colors shadow-sm"
                >
                    Generate QR Code
                </button>
            </div>

            <!-- Right Preview & Download Area -->
            <div class="flex flex-col items-center justify-center space-y-6">
                <!-- Preview Box -->
                <div class="w-full aspect-square border border-gray-200 rounded-2xl p-6 flex items-center justify-center bg-white shadow-inner">
                    <div id="qrcode-container" class="flex items-center justify-center"></div>
                </div>

                <!-- Download Button (1000x1000 Canvas Export) -->
                <button 
                    id="download-btn"
                    onclick="downloadQRCode()" 
                    disabled 
                    class="w-full flex items-center justify-center gap-2 border border-gray-300 bg-white text-slate-700 font-semibold py-3 px-4 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download PNG (1000x1000)
                </button>
            </div>

        </div>
    </main>

    <!-- Client-side Logic -->
    <script>
        let activeTab = 'URL';
        let qrcodeInstance = null;

        function setTab(tab) {
            activeTab = tab;
            const urlBtn = document.getElementById('tab-url');
            const textBtn = document.getElementById('tab-text');
            const label = document.getElementById('input-label');
            const input = document.getElementById('qr-input');

            if (tab === 'URL') {
                urlBtn.className = "px-5 py-1.5 text-sm font-semibold rounded-md bg-white text-slate-900 shadow-sm transition-all";
                textBtn.className = "px-5 py-1.5 text-sm font-medium text-gray-500 rounded-md hover:text-slate-900 transition-all";
                label.innerText = "Destination URL";
                input.placeholder = "https://example.com";
            } else {
                textBtn.className = "px-5 py-1.5 text-sm font-semibold rounded-md bg-white text-slate-900 shadow-sm transition-all";
                urlBtn.className = "px-5 py-1.5 text-sm font-medium text-gray-500 rounded-md hover:text-slate-900 transition-all";
                label.innerText = "Text Content";
                input.placeholder = "Masukkan teks di sini...";
            }
        }

        function generateQRCode() {
            const inputVal = document.getElementById('qr-input').value.trim();
            const container = document.getElementById('qrcode-container');
            const downloadBtn = document.getElementById('download-btn');

            if (!inputVal) {
                alert('Silakan masukkan ' + (activeTab === 'URL' ? 'URL' : 'teks') + ' terlebih dahulu!');
                return;
            }

            container.innerHTML = "";

            // Rendering preview client-side
            qrcodeInstance = new QRCode(container, {
                text: inputVal,
                width: 200,
                height: 200,
                colorDark: "#000000",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.H
            });

            downloadBtn.disabled = false;
        }

        function downloadQRCode() {
            const inputVal = document.getElementById('qr-input').value.trim();
            if (!inputVal) return;

            // Membuat canvas tersembunyi untuk ekspor ukuran 1000x1000
            const tempDiv = document.createElement('div');
            tempDiv.style.display = 'none';
            document.body.appendChild(tempDiv);

            const tempQr = new QRCode(tempDiv, {
                text: inputVal,
                width: 1000,
                height: 1000,
                colorDark: "#000000",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.H
            });

            // Tunggu render canvas selesai
            setTimeout(() => {
                const img = tempDiv.querySelector('img');
                const canvas = tempDiv.querySelector('canvas');
                let dataUrl = "";

                if (canvas) {
                    dataUrl = canvas.toDataURL("image/png");
                } else if (img) {
                    dataUrl = img.src;
                }

                if (dataUrl) {
                    const link = document.createElement('a');
                    link.href = dataUrl;
                    link.download = `qrcode_1000x1000.png`;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }

                document.body.removeChild(tempDiv);
            }, 100);
        }

        // Default QR Code saat pertama kali dimuat
        window.onload = function() {
            generateQRCode();
        };
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True)