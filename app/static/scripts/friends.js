var global_reminder_id
let ul = document.getElementById('friends_list_modal');

function open_friends_list(index) {
    if (online()){
        event.stopPropagation()
        global_reminder_id = index
        ul.classList.remove('hidden')
    }
}

function close_friends_list() {
    ul.classList.add('hidden')
}

document.addEventListener('click', close_friends_list)

function send_rem_to_friend(friend_id){
    return
}

function add_friend(){
    return
}
    
async function friends_dynamic_list(rem_id){
    let result = await fetch("/friends")
    const response = await result.json();
    if (response == ""){
        let li = document.createElement("li");
        li.innerHTML = "Vous n'avez pas encore d'amis. Ajoutez en !";
        li.style = "padding-bottom: 5px;"
        li.addEventListener('click', (event) => {
            add_friend()
        })
        ul.appendChild(li);
    }
    else {
        response.forEach(friend => {
            let li = document.createElement("li");
            li.innerHTML = friend.username;
            li.addEventListener('click', (event) => {
                send_rem_to_friend(friend.id)
            })
            ul.appendChild(li);
        });
        let li = document.createElement("li");
        li.innerHTML = "Plus +";
        li.addEventListener('click', (event) => {
            add_friend()
        })
        ul.appendChild(li);
    }   
};


friends_dynamic_list()