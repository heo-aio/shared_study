let users = [];
let next_user_id = 1;

const increase_user_id = function(){
    return next_user_id++;
}

module.exports ={
    users,
    increase_user_id
};