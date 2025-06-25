var global_reminder_id
let ul = document.getElementById('friends_list_modal');

let div = document.getElementById('add_friend_modal')
let input = div.querySelector('input')
let friend_form = div.querySelector('form')
let alert_box = div.querySelector('div')
let span = document.getElementById('friend_username_span')

let notif_div = document.getElementsByClassName('notification_friend')[0]
let friend_username = notif_div.querySelector('i')
let ok_button = notif_div.querySelector('button')


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

function open_close_add_friend(){
    div.classList.toggle('hidden')
    input.value = "";
}

function open_close_notification_friend(){
    notif_div.classList.toggle('hidden')
    friend_username.value = "";
}

ok_button.addEventListener('click', open_close_notification_friend)



function send_rem_to_friend(friend_id){
    return
}



friend_form.addEventListener('submit',  async (event) => {
    event.preventDefault();  // Prevent the default form submission
    add_friend()

})

async function add_friend(){
    // Make a POST request to the server
    let result = await fetch("/friend", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"username": input.value})
    });
    
    if (result.ok) {
        open_close_add_friend()
        open_close_notification_friend()
        friend_username.innerHTML = input.value
        input.value = "";
        alert_box.classList.add("hidden")
    } else {
        if (result.status == 404){
            alert_box.classList.remove("hidden")
            span.innerHTML = input.value
        } else {
            alert(`Error ${result.status}: ${result.statusText}`)
        }
    }
        
}
    


async function friends_dynamic_list(rem_id){
    let result = await fetch("/friends")
    const response = await result.json();
    if (response == ""){
        let li = document.createElement("li");
        li.innerHTML = "Vous n'avez pas encore d'amis. Ajoutez en !";
        li.style = "padding-bottom: 5px;"
        li.addEventListener('click', (event) => {
            open_close_add_friend()
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
            open_close_add_friend()
        })
        ul.appendChild(li);
    }   
};


friends_dynamic_list()