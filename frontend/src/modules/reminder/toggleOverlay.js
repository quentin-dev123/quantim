import styles from "../../style/reminder.module.css"

export function toggleOverlay(id) {
    const overlay = document.getElementById(`overlay${id}`);
    const remDiv = document.getElementById(`remDiv${id}`);
    const container = document.getElementById(`container${id}`);
    
    overlay.classList.toggle(styles.active);
    remDiv.classList.toggle(styles.disable_content);
    container.classList.toggle(styles.container_zoom);
}