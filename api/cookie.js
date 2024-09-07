import Cookies from 'js-cookie';

// 서버로부터 받은 토큰
const token = '서버로부터 받은 토큰';

// 쿠키에 토큰 저장
Cookies.set('token', token);