let timeoutId;

export function oc_top_bar_icons(id, event) {
    event.stopPropagation()
    const top_bar_icons = document.getElementById("top_bar_icons" + id)
    const expand = document.getElementById("expand" + id)
    const outer_pin_icon = document.getElementById("outer_pin_icon" + id);
    if (top_bar_icons.style.height == "0px"){
        top_bar_icons.style.height = "33px";
        timeoutId = setTimeout(() => {
        outer_pin_icon.classList.add('hidden');
        expand.innerHTML = "expand_less";
        }, 300);
    }
    else {
        close_top_bar_icons(id, event)
    }
}

export function close_top_bar_icons(id, event) {
    event.stopPropagation()
    const top_bar_icons = document.getElementById("top_bar_icons" + id)
    const expand = document.getElementById("expand" + id)
    const outer_pin_icon = document.getElementById("outer_pin_icon" + id);
    top_bar_icons.style.height = "0";
    expand.innerHTML = "expand_more";
    if (outer_pin_icon.classList.contains('active')){
    outer_pin_icon.classList.remove('hidden');
    }
}