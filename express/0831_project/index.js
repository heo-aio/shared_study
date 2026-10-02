const express = require('express');
const app = express();
const PORT = 80;
const posts = require("./routes/posts");
const auth = require("./routes/auth");

app.use(express.json());
app.use("/posts", posts);
app.use("/users", auth);

app.get('/', (req, res) => {
    res.send('Project 서버 작동 ing');
})

app.listen(PORT, ()=>{
    console.log(`http://localhost:${PORT}`);
})