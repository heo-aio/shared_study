const exporess = require('express'); //express 모듈 호출
const app = exporess(); // express를 객체화하여 app에 할당

// 겟방식으로 "/"" 요청이 오면... 할 일
// btn.addEventListener('click', function(evt){}); 
app.get('/', (req, res)=>{
    res.send('Hello, World Express.js');
});

// 서버는 8000번 포트로 실행
app.listen(8000, function(){
    console.log('server on : http://localhost:8000'); // 서버가 켜졌을 때, 띄울 문구
});

// node index.js