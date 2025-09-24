import styles from "../style/reminder.module.css"
import adjustColorBrightness from "../modules/adjustColor.js";

export default function Reminder(props){
    return (
    <div style={styles.container} id={`container${props.id}`}>
        <div style={Object.assign({}, styles.reminder_container, {backgroundColor: props.subjectColor})} id={`remDiv${props.id}`}>
            <a style={Object.assign({}, styles.remindera, {backgroundColor: props.tagColor})} id={`rema${props.id}`}>{props.tag}</a>
            <nobr style={styles.remindernobr} id={`remnobr${props.id}`}>Pour : {props.date}</nobr>
            <h2 style={Object.assign({}, styles.reminderh2, {backgroundColor: adjustColorBrightness(props.tagColor, 70)})} id={`remh2${props.id}`}>{props.subject}</h2>adjustColorBrightness
            <p style={styles.reminderp} id={`remp${props.id}`}>{props.content}</p>
        </div>
    </div>
    );
}