import styles from "../style/reminder.module.css"
import adjustColorBrightness from "../modules/adjustColor.js";
import { icons } from "../modules/stylesheets.js";

export default function Reminder(props){
    icons()
    return (
    <div 
        className={styles.container} 
        id={`container${props.id}`}
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
            <div className="hidden">
                <span
                    className={`material-icons ${styles.icon} ${styles.outer_pin} hidden`}
                    id={`outer_pin_icon${props.id}`}
                >push_pin
                </span>
                <span 
                    className={`fa-solid fa-paper-plane ${styles.icon} ${styles.link}`}
                    id={`link_icon${props.id}`}
                >
                </span>
            </div>
        </div>
    </div>
    );
}