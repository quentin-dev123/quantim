import { close_top_bar_icons } from "./top_bar_icons";
import { toggleOverlay } from "./toggleOverlay";

export function remClick(id, event){
    event.stopPropagation()
    const top_bar_icons = document.getElementById("top_bar_icons" + id)
    if (top_bar_icons.style.height == "0px"){
        toggleOverlay(id);
    }
    else {
        close_top_bar_icons(id, event)
    }
}