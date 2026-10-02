// 5. 회원가입 -> 라이브러리 install 필요
// -> bcrypt : pw 암호화하기 위한 라이브러리, jsonwebtoken : JWT토큰 생성 및 검증을 위한 라이브러리

const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const {users, increase_user_id} = require("../data/users");
const jwt = require("jsonwebtoken");
const {JWT_SECRET} = require("../config");

// 회원가입
router.post("/join", async (req, res) => {
    const {userId, pw} = req.body;

    if (!userId || !pw){
        return res.json({"success": false, "msg" : "아이디와 비밀번호는 필수입니다."});
    }

    const duplication = users.find((item)=>{
        return item.userId === userId;
    });
    if (duplication){
        return res.json({"success" : false, "msg" : "이미 존재하는 아이디입니다."});
    }

    const hashPw = await bcrypt.hash(pw, 10);

    const newUser = {
        id: increase_user_id(),
        userId,
        pw: hashPw
    }

    users.push(newUser);
    return res.json({"success": true, "msg" : "회원가입 성공"});
});

// 로그인
router.post("/login", async function(req, res){
    const {userId, pw} = req.body;

    if (!userId || !pw){
        return res.json({"success": false, "msg" : "아이디와 비밀번호는 필수 입력 항목입니다."});
    }

    const user = users.find((item)=>{
        return item.userId === userId;
    })

    // 입력한 아이디가 존재하는지
    if (!user){
        return res.json({"success": false, "msg" : "아이디를 확인해주세요."});
    }

    // 비밀번호 비교 (암호화된 값이라 직접 비교 불가, bcrypt.compare 사용)
    const certification = await bcrypt.compare(pw, user.pw);
    if (!certification){
        return res.json({"success": false, "msg" : "비밀번호를 확인해주세요."});
    }

    const token = jwt.sign({userId}, JWT_SECRET, {expiresIn: "30m"});

    return res.json({"success": true, "msg" : "로그인 성공.", "token": token});
})

module.exports = router;