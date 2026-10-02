const express = require('express');
const router = express.Router();
const {posts, increase_id} = require('../data/posts');

// 1. 리스트 보기 (메인 첫 화면)
router.get("/", (req, res) => {
    return res.json(posts);
})

// 그냥 검색하는거 만들어봄
router.get("/search", (req, res) => {
    console.log(req.query);
    const {title} = req.query;
    // const result = title;
    let result;

    if (title){
        result = posts.filter(function(item){
            return item.title.includes(title);
        })
    }else{
        return res.send("검색 결과가 없습니다.")
    }

    return res.json({"검색 결과:": result});
})

// 2. 특정 글 상세보기
router.get("/:id", (req, res) => {
    const id = req.params.id;
    const post = posts.find((item)=>{
        return item.id === parseInt(id);
    });

    if (post === undefined) {
        return res.json({"success": false, "msg": "글이 없습니다."})
    }

    return res.json({"success": true, post: post, "msg": "특정 글 보기 성공"});
})

// 3. 글 작성
router.post("/", (req, res) => {
    const {title, content, author} = req.body;

    if (!title || !content) {
        return res.json({"success":false, "msg": "제목과 내용은 필수로 입력해야 합니다."});
    }

    const newPost = {
        id: increase_id(),
        title,
        content,
        author
    }

    posts.push(newPost);
    res.json({"success" : true, "msg" : "글쓰기 성공", "newPost" : newPost});
})

// 4. 글 삭제하기
router.delete("/:id", function(req, res){
    const {id} = req.params;
    const post_id = parseInt(id);

    // 못 찾으면 find()는 undefined, findIndex()는 **-1**을 반환
    const idx = posts.findIndex(function(item){
        return item.id === post_id;
    });

    if (idx < 0){
        return res.json({"success" : false, "msg" : "글이 없습니다."});
    }

    posts.splice(idx, 1);
    return res.json({"success" : true, "msg" : "삭제 성공"});
})


module.exports = router;