// Online vs offline functions
var online_variable = true
function went_online(){
    online_variable = true
    alert("Vous êtes à nouveau en ligne")
}

function went_offline(){
    online_variable = false
    alert("Vous êtes hors ligne, certaines fonctionnalités ne fonctionneront plus")
}

function offline_alert(){
    alert("Cette fonctionnalité ne fonctionne pas hors ligne")
}

function online(){
  if (online_variable){
    return true
  } else {
    offline_alert()
    return false
  }
}

function open_link(link){
  if (online()){
    window.location.href = link
  }
}


window.addEventListener("online", went_online);
window.addEventListener("offline", went_offline);