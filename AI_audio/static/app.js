document.addEventListener('DOMContentLoaded', function() {
    const apiKeyInput = document.getElementById('apiKey');
    const connectBtn = document.getElementById('connectBtn');
    const recordButton = document.getElementById('recordButton');
    const audioOutput = document.getElementById('audioOutput');
    
    // 设置默认的 API Key
    apiKeyInput.value = '16e16f545ddb768486d2a4892453722a.VEKjDjvnoDN9Iifc';
    
    let ws = null;
    let mediaRecorder = null;
    let audioChunks = [];
    let isRecording = false;

    // 连接 WebSocket
    connectBtn.addEventListener('click', async function() {
        const apiKey = apiKeyInput.value;
        
        try {
            const response = await fetch('/connect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ api_key: apiKey })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // 建立 WebSocket 连接
                ws = new WebSocket(`ws://${window.location.host}/ws`);
                
                ws.onopen = () => {
                    ws.send(JSON.stringify({ api_key: apiKey }));
                    recordButton.disabled = false;
                    connectBtn.textContent = '已连接';
                    connectBtn.disabled = true;
                };
                
                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    if (data.type === 'audio') {
                        // 处理音频数据
                        const audio = new Audio(`data:audio/wav;base64,${data.audio}`);
                        audioOutput.style.display = 'block';
                        audioOutput.src = `data:audio/wav;base64,${data.audio}`;
                        audioOutput.play();
                    }
                };
                
                ws.onerror = (error) => {
                    console.error('WebSocket错误:', error);
                };
                
                ws.onclose = () => {
                    recordButton.disabled = true;
                    connectBtn.textContent = '开始体验';
                    connectBtn.disabled = false;
                };
                
            } else {
                alert('连接失败: ' + data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('连接失败');
        }
    });

    // 录音功能
    recordButton.addEventListener('click', async function() {
        if (!isRecording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                
                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };
                
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const formData = new FormData();
                    formData.append('audio', audioBlob);
                    formData.append('api_key', apiKeyInput.value);
                    
                    try {
                        const response = await fetch('/upload-audio', {
                            method: 'POST',
                            body: formData
                        });
                        
                        if (!response.ok) {
                            throw new Error('音频上传失败');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('音频上传失败');
                    }
                };
                
                mediaRecorder.start();
                isRecording = true;
                recordButton.classList.add('recording');
                recordButton.querySelector('i').classList.remove('fa-microphone');
                recordButton.querySelector('i').classList.add('fa-stop');
                
            } catch (error) {
                console.error('Error:', error);
                alert('无法访问麦克风');
            }
        } else {
            mediaRecorder.stop();
            isRecording = false;
            recordButton.classList.remove('recording');
            recordButton.querySelector('i').classList.remove('fa-stop');
            recordButton.querySelector('i').classList.add('fa-microphone');
        }
    });
}); 