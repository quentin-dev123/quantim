import styles from "../style/reminder.module.css"
import adjustColorBrightness from "../modules/adjustColor.js";
import { icons, fonts } from "../modules/stylesheets.js";
import { oc_top_bar_icons } from "../modules/reminder/top_bar_icons.js";
import { remClick } from "../modules/reminder/remClick.js";

export default function Reminder(props){
    icons(); fonts();
    return (
    <div 
        className={styles.container} 
        id={`container${props.id}`}
        onClick={event => remClick(props.id, event)}
    >
        <div 
            className={styles.reminder_container}
            style={{backgroundColor: props.subjectColor}} 
            id={`remDiv${props.id}`}
        >
            <a 
                className={styles.remindera}
                style={{backgroundColor: props.tagColor}} 
                id={`rema${props.id}`}
            >{props.tag}
            </a>
            <nobr 
                className={styles.remindernobr} 
                id={`remnobr${props.id}`}
            >Pour : {props.date}
            </nobr>
            <h2 
                className={styles.reminderh2}
                style={{backgroundColor: adjustColorBrightness(props.tagColor, 70)}} 
                id={`remh2${props.id}`}
            >{props.subjectName}
            </h2>
            <p 
                className={styles.reminderp} 
                id={`remp${props.id}`}
            >{props.content}
            </p>

            <input
                className={styles.reminderinput}
                id={`reminput${props.id}`}
                type="checkbox"
            >
            </input>
            <span
                className={`material-icons ${styles.icon} ${styles.outer_pin} ${styles.hidden}`}
                id={`outer_pin_icon${props.id}`}
            >push_pin
            </span>
            <div 
                className={styles.top_bar_icons} 
                id={`top_bar_icons${props.id}`} 
                style={{height: "0px"}}
            >
                <div 
                    className={styles.reminderdiv}
                    id={`remdiv${props.id}`}
                >
                    <span 
                        className={`material-icons ${styles.icon}`}
                        id={`remspan${props.id}`} 
                        style={{visibility: "hidden"}}
                    >expand_less
                    </span>
                    <span 
                        className={`material-icons ${styles.icon} ${styles.pin}`} 
                        id={`pin_icon${props.id}`}
                    >push_pin
                    </span>
                    <span 
                        className={`fa-solid fa fa-paper-plane ${styles.icon} ${styles.link}`} 
                        id={`link_icon${props.id}`}
                    >
                    </span>
                </div>
            </div>
            <span 
                className={`material-icons ${styles.icon} ${styles.expand}`}
                id={`expand${props.id}`}
                onClick={event => oc_top_bar_icons(props.id, event)}
            >expand_more
            </span>
        </div>
        <div 
            className={`${styles.overlay} ${styles.buttons_overlay}`} 
            id={`overlay${props.id}`}
        >
            <button 
                className={styles.edit}
                id={`edit${props.id}`}
            >Modifier
            </button>
            <button 
                className={styles.del}
                id={`del${props.id}`}
            >Effacer
            </button>
        </div>
    </div>
    );
}