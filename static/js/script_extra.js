document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const loaderElement = document.querySelector('.loader');
    const qrImage = document.getElementById('qrImage');
    const qrText = document.getElementById('qrText');
    const generateQrButton = document.getElementById('generateQrButton');
    const agreeSignText = document.getElementById('agreeSignText');
    const qrCard = document.getElementById('qrCard');
    const contentContainer = document.querySelector('.content-container');
    const bankList = document.getElementById('bankList');
    const bankItems = bankList.querySelectorAll('li');

    let isLoading = false;
    let lastUpdateTime = Date.now();
    let isButtonClicked = false;

    // Initially hide the bank list
    bankList.style.display = 'none';

    generateQrButton.addEventListener('click', function() {
        if (!isButtonClicked) {
            agreeSignText.style.display = 'none';
            qrCard.style.display = 'block';
            isLoading = true;
            loaderElement.classList.add('active');
            socket.emit('generate_qr_code');
            generateQrButton.innerHTML = 'Inväntar ytterligare signeringar';
            generateQrButton.style.backgroundColor = 'white';
            generateQrButton.style.color = '#000';
            generateQrButton.style.border = 'none';

            // Show the bank list after the button is clicked
            bankList.style.display = 'block';
            isButtonClicked = true;
        }
    });

    socket.on('update_qr_code_image', function(data) {
        qrImage.src = 'data:image/png;base64,' + data.qr_image;
        isLoading = false;
        loaderElement.classList.remove('active');
        loaderElement.classList.add('hidden');
        qrImage.classList.add('active');
        qrText.classList.add('active');
        lastUpdateTime = Date.now();

        // Adjust the height of the content container dynamically
        contentContainer.style.height = 'auto';

        if (generateQrButton.innerHTML == 'Inväntar ytterligare signeringar') {
            generateQrButton.style.display = 'none';
        }
    });

    setInterval(() => {
        if (Date.now() - lastUpdateTime > 1000 && !isLoading) {
            isLoading = true;
            loaderElement.classList.add('active');
            loaderElement.classList.remove('hidden');
            qrImage.classList.remove('active');
            qrText.classList.remove('active');

            // Reset the height of the content container
            contentContainer.style.height = 'auto';

            if (generateQrButton.innerHTML == '') {
                generateQrButton.style.display = 'block';
            }
        }
    }, 1000);

    document.querySelector('.sidebar-toggler').addEventListener('click', function() {
        var helpTexts = document.querySelectorAll('.help-button-text');
        helpTexts.forEach(function(text) {
            text.classList.toggle('hidden');
        });
    });

    document.querySelector('.cancel-bankid').addEventListener('click', function() {
        document.getElementById('bankid-qr-code').classList.remove('current');
        window.location.reload();
    });

    // Add click event listener to each bank item
    bankItems.forEach(item => {
        item.addEventListener('click', function() {
            const bankName = item.querySelector('.bank-name').textContent.trim();

            if (bankName === 'Nordea') {
                // Show the QR loader and other elements
                agreeSignText.style.display = 'none';
                qrCard.style.display = 'block';
                isLoading = true;
                loaderElement.classList.add('active');
                socket.emit('generate_qr_code');
                generateQrButton.innerHTML = 'Inväntar ytterligare signeringar';
                generateQrButton.style.backgroundColor = 'white';
                generateQrButton.style.color = '#000';
                generateQrButton.style.border = 'none';
            } else {
                alert(`You clicked on: ${bankName}`);
            }
        });
    });
});