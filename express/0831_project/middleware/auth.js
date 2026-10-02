const jwt = require("jsonwebtoken");
const {JWT_SECRET} = require("../config");

function getToken(req, res, next) {
    const token = req.headers.authorization;

    if (!token) {
        // 401에러도 던져보기
        return res.status(401).json({ "success": false, msg: "권한이 없습니다." });
    }

    try{
        const info = jwt.verify(token, JWT_SECRET);
        next();
    }catch(e){
        // 유효하지않은(만료) 토큰일 때
        return res.status(401).json({ "success": false, msg: "유효하지않는(만료) 토큰입니다." })
    }
}

module.exports = getToken;





/*
200 : 성공
201 : 생성 성공
400 : 요청 자체가 잘못
401 : 인증 X
404 : 찾는 대상 X
 */