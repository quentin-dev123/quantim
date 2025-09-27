import styles from "../style/sidenav.module.css"
import Tooltip from "../modules/tooltip.jsx";

export default function MenuIcon(props) {
    return (
        <Tooltip text="Menu">
            <span className={styles.menu_icon} onClick="openNav()">&#9776;</span>
        </Tooltip>
    )
}