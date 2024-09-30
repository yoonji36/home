document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // 기본 폼 제출 방지

    const formData = new FormData(this);
    const loginData = {
        username: formData.get('username'),
        password: formData.get('password')
    };

    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData),
        });

        const result = await response.json();
        if (response.ok) {
            document.getElementById('login-message').innerText = '로그인 성공!';
        } else {
            document.getElementById('login-message').innerText = result.message || '로그인 실패';
        }
    } catch (error) {
        document.getElementById('login-message').innerText = '서버 오류 발생';
    }
});
