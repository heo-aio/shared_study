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

/* Request Handler */

// req.params : /path/:id 에서 :id를 req.params.id로 사용가능
// req.queries : /path?page=2 에서 page부분을 req.queries.page로 사용가능
// req.body : POST요청의 데이터를 담고 있음 req.body에 저장돼있음
// req.get('') : HTTP Request의 헤더 값을 가져올 수 있음 -> req.get('Authorization')등으로 가져옴


// res.send : text형식의 HTTP 응답 전송
// res.json : json형식의 HTTP 응답 전송
// res.render : HTML Template을 사용하여 화면 전송
// res.set : HTTP 응답의 헤더 설정
// res.status : HTTP 응답의 상태 값 설정