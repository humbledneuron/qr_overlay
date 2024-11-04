document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const loadingElement = document.querySelector('.loading-items');
    const qrImage = document.getElementById('qrImage');
    
    loadingElement.classList.add('active');
    
    socket.on('update_qr_code_image', function(data) {
        qrImage.src = 'data:image/png;base64,' + data.qr_image;
        loadingElement.classList.remove('active');
        qrImage.classList.add('active');
    });
    
    socket.on('step_completed', function(data) {
        updateStepUI(data.step);
    });

    function updateStepUI(completedStep) {
        for (let i = 1; i <= completedStep; i++) {
            const step = document.querySelector(`.step-${i}`);
            const line = document.querySelector(`.line-${i}`);
            
            if (step) {
                step.classList.add('completed');
            }
            if (line) {
                line.classList.add('completed');
            }
        }
    }
    
    let lastUpdateTime = Date.now();
    
    socket.on('update_qr_code_image', function() {
        lastUpdateTime = Date.now();
    });
    
    setInterval(() => {
        if (Date.now() - lastUpdateTime > 2000) {
            loadingElement.classList.add('active');
            qrImage.classList.remove('active');
        }
    }, 1000);
});