let posts = [
    { id: 1, title: "첫 번째 글", content: "안녕하세요", author: "허정모" },
    { id: 2, title: "두 번째 글", content: "테스트", author: "관리자" },
];

let nextId = 3; // 새 글 작성할 때 쓸 id 카운터

const increase_id = ()=>{
    return nextId++;
}

module.exports = { posts, increase_id };