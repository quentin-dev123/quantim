var global_reminder_id
let ul = document.getElementById('friends_list_modal');

function open_friends_list(index) {
    event.stopPropagation()
    global_reminder_id = index
    ul.classList.toggle('hidden')
}


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