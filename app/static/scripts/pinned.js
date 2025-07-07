async function pin(reminder_id, container_id){
    try {
        event.stopPropagation()
    } catch (e) {}
    try {
        if (online()){
            const pin_icon = document.getElementById(`pin_icon${container_id}`);
            const outer_pin_icon = document.getElementById(`outer_pin_icon${container_id}`);

            let message;
            if (pin_icon.classList.contains("active")){
                message = await patch("/api/reminder/pinned/" + reminder_id + "/False")
            } else {
                message = await patch("/api/reminder/pinned/" + reminder_id + "/True")
            }

            if (message.ok){
                pin_icon.classList.toggle('active');
                outer_pin_icon.classList.toggle('active');
                try {
                    open_top_bar_icons(container_id, event)
                } catch (e) {}
            } else {
                alert(message.statusText)
            }

        }
    } catch(error){
        alert('Error: ' + error)
    }
}