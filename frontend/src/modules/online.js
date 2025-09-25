// Online vs offline functions
var online_variable = true
function isPageVisible() {
  return document.visibilityState === 'visible';
}
    
function went_online(){
    online_variable = true
    if (isPageVisible()){
      alert("Vous êtes à nouveau en ligne")
    }
}

function went_offline(){
    online_variable = false
    if (isPageVisible()){
      alert("Vous êtes hors ligne, certaines fonctionnalités ne fonctionneront plus")
    }
}

function offline_alert(){
    alert("Cette fonctionnalité ne fonctionne pas hors ligne")
}

export function online(){
  if (online_variable){
    return true
  } else {
    offline_alert()
    return false
  }
}

export function open_link(link){
  if (online()){
    window.location.href = link
  }
}


window.addEventListener("online", went_online);
window.addEventListener("offline", went_offline);