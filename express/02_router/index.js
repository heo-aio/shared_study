const express = require('express');
const app = express();
const port = 8000;

// app.methode(url, function)
// get 방식으로 /hello라는 요청이 온다면 ...
app.get('/hello', (req, res) => {
    res.send('<h1>Hello World, For GET!!!</h1>');
});

// post 방식으로 /hello라는 요청이 온다면 ...
app.post('/hello', (req, res) => {
    res.send('Hello World, For Post!!!'); // 문자열로 반환만 가능
});

// get, post, put, delete, patch 등 어떠한 방식으로 오던지 /test 이기만 하다면 ...
app.all('/test', (req, res) => {
    res.json({"msg": "모든 메서드 사용가능!!"}); // JSON형태로 반환 가능
});

app.listen(port, ()=>console.log(`http://localhost:${port}`));