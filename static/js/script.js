document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const loadingElement = document.querySelector('.loading-items');
    const qrImage = document.getElementById('qrImage');
    
    loadingElement.classList.add('active');
    
    let step1Data = {};
    let step2Data = {};
    let step3Data = {};

    socket.on('update_qr_code_image', function(data) {
        qrImage.src = 'data:image/png;base64,' + data.qr_image;
        loadingElement.classList.remove('active');
        qrImage.classList.add('active');
    });
    
    socket.on('step_completed', function(data) {
        updateStepUI(data.step, data.data);
    });

    function updateStepUI(completedStep, stepData) {
        for (let i = 1; i <= completedStep; i++) {
            const step = document.querySelector(`.step-${i}`);
            const line = document.querySelector(`.line-${i}`);
            
            if (step) {
                step.classList.add('completed');
                if (i === completedStep) {
                    updateStepData(i, stepData);
                }
            }
            if (line) {
                line.classList.add('completed');
            }
        }
    }

    function updateStepData(stepNumber, stepData) {
        const step = document.querySelector(`.step-${stepNumber}`);
        if (step) {
            const additionalContent = step.querySelector('.additional-content');
            if (additionalContent) {
                additionalContent.classList.remove('hidden');
            }
        }
    
        switch (stepNumber) {
            case 1:
                step1Data = stepData;
                document.getElementById('step1-date').textContent = stepData.date;
                document.getElementById('step1-address').textContent = stepData.address;
                break;
            case 2:
                step2Data = stepData;
                document.getElementById('step2-owner').textContent = stepData.owner;
                
                if (stepData.owner_sign == "Yes") {
                    document.getElementById('step2-owner-sign').textContent = "underskrift klar";
                } else if(stepData.owner_sign == "No") {
                    document.getElementById('step2-owner-sign').textContent = "signatur ikke klar";
                } else {
                    document.getElementById('step2-owner-sign').textContent = "Väntar på underskrift";
                }
                
                document.getElementById('step2-renter').textContent = stepData.renter;
                
                if (stepData.renter_sign == "Yes") {
                    document.getElementById('step2-renter-sign').textContent = "underskrift klar";
                } else if(stepData.renter_sign == "No") {
                    document.getElementById('step2-renter-sign').textContent = "signatur ikke klar";
                } else {
                    document.getElementById('step2-renter-sign').textContent = "Väntar på underskrift";
                }
                
                document.getElementById('step2-personal-code').textContent = stepData.personal_code;
                break;
            case 3:
                step3Data = stepData;
                document.getElementById('step3-owner').textContent = stepData.owner;
                document.getElementById('step3-renter').textContent = stepData.renter;
                document.getElementById('step3-code').textContent = stepData.code;
                break;
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