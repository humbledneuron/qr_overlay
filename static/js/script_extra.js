document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const loaderElement = document.querySelector('.loader');
    const qrImage = document.getElementById('qrImage');
    const qrText = document.getElementById('qrText');
    const generateQrButton = document.getElementById('generateQrButton');
    const agreeSignText = document.getElementById('agreeSignText');
    const qrCard = document.getElementById('qrCard');
    const contentContainer = document.querySelector('.content-container');

    let isLoading = false;
    let lastUpdateTime = Date.now();

    generateQrButton.addEventListener('click', function() {
        agreeSignText.style.display = 'none';
        qrCard.style.display = 'block';
        isLoading = true;
        loaderElement.classList.add('active');
        socket.emit('generate_qr_code');
        generateQrButton.innerHTML = 'Inväntar ytterligare signeringar';
        generateQrButton.style.backgroundColor = 'white';
        generateQrButton.style.color = '#000';
        generateQrButton.style.border = 'none';
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
            generateQrButton.innerHTML = '';
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
                generateQrButton.innerHTML = 'Inväntar ytterligare signeringar';
            }
        }
    }, 1000);
});