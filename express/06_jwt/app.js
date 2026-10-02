// express, JWT, 암호화 관련
// npm install express jsonwebtoken bcrypt

const express = require('express');
const app = express();
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

app.use(express.json());
// app.use(cors());

// 서버를 켤 때 마다 새로 생성
const KEY = crypto.randomBytes(64).toString('hex');
console.log("sing key : ", KEY);

app.post('/login', (req, res) => {
    const {id, pw} = req.body;
    console.log(`${id}와 ${pw}를 이용해 db안에 회원이 있는지 확인`);
    // 로그인 했다고 가정하고 실습
    // 토큰 생성 (payload, key, expire)
    // s, m, h, d, w, y, 1.5h 등 소수점도 가능
    const token = jwt.sign({id, pw}, KEY, {expiresIn: '30m'});
    res.json({'success': true, 'token': token})
});

app.post('/check', (req, res) => {
    const headers = req.headers;
    console.log("header : ", headers);
    const token = headers.authorization;

    if (token == null){
        return res.json({'loginYN': false, 'msg': '토큰이 없습니다.'});
    }
    console.log('확인용 콘솔 ...')

    try{
        const info = jwt.verify(token, KEY); // 토큰 검증 verify
        console.log('info', info);
        // 요청했던 일을 한다.
        return res.json({'loginYN': true, 'data': '추가작업 결과'});
    }catch(e){
        // 만료된 토큰이라면 에러가 발생한다.
        return res.json({'loginYN': false, 'msg':'유효하지 않은 토큰입니다.'})
    }

    res.json({loginYN: true});
});

app.listen(80, ()=>console.log("http://localhost"));