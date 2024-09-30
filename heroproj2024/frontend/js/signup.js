document.getElementById('signupForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // 기본 폼 제출 방지

    const formData = new FormData(this);
    const signupData = {
        username: formData.get('username'),
        password: formData.get('password'),
        height: formData.get('height'),
        weight: formData.get('weight'),
        bloodPressure: formData.get('bloodPressure')
    };

    try {
        const response = await fetch('/api/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(signupData),
        });

        const result = await response.json();
        if (response.ok) {
            document.getElementById('signup-message').innerText = '회원가입 성공!';
        } else {
            document.getElementById('signup-message').innerText = result.message || '회원가입 실패';
        }
    } catch (error) {
        document.getElementById('signup-message').innerText = '서버 오류 발생';
    }
});
