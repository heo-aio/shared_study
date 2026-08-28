const express = require('express');
const router = express.Router();
const Member = require('./model');

// 회원 가입(/member/join)
router.post('/join', async (req, res)=>{

    const {id, pw, name, phone} = req.body;

    try{
        // await Member.create({id:id, pw:pw, name:name, phone:phone}); // key value값이 같으면 생략가능 (아래처럼)
        let result = await Member.create({id, pw, name, phone});
        let object = result.toObject();
        delete object.pw; // pw는 결과값에서 제거하고 보여준다.
        // object.pw = ''
        res.json({'join success':true, 'data': object});

    }catch(e) {
        console.error(e, 'CODE : '+ e.code);

        let msg = "";

        switch (e.code) {
            case 11000:
                msg = "이미 사용중인 아이디 입니다.";
                break;

            default:
                msg = "필수 값을 확인해 주세요";
        }
        res.json({'success': false, message:msg});
    }
});

// 회원 리스트(/member/list, /member/)
router.get(['/list', '/'], async function(req, res){
    let list = await Member.find()
        .sort({'createdAt': 1}) // 생성일 내림차순으로 정렬
        .lean(); // 순수 JSON으로 반환

    res.json({'list success': true, 'data': list});
});

// 회원 정보 상세보기(/member/get/:id)
router.get('/get/:id', async (req ,res) =>{
    const {id} = req.params;
    // 찾는 내용이 하나일 경우는 findOne({filter}) 사용
    let member = await Member.findOne({id:id}).lean()

    if (member == null){
        res.json({'success': false, 'data': {'info':{}, 'msg': '존재하지 않는 회원'}});
    }
    res.json({'view success':true, 'id':member, 'msg':'상세보기 완료'});
});

// 회원정보 수정(/member/update/:id)
router.put('/update/:id', function(req, res){
    const {id} = req.params;
    const param = req.body;
    res.json({'update success':true, 'id':id, 'msg': param});
});

// 회원 삭제(/member/delete/:id)
router.delete('/delete/:id', async (req, res)=>{
    let {id} = req.params;
    let member = await Member.findOneAndDelete({id}).lean();
    if (member == null){
        res.json({'success':false, 'msg': '회원 없음'});
    }
    res.json({'success':true, 'msg': '회원 삭제 완료', data:member});
});

module.exports = router;