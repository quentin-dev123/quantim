import styles from "../style/agenda.module.css"
import Base from "../components/base"
import Reminder from "../components/Reminder";
import Reminders from "../components/Reminders";
import { open_link } from "../modules/online.js";

export default function Agenda(){
    return <>
    <Base header="Agenda Personnel" topIcons={true}>
        <a className={styles.add_rem_button} onClick={() => open_link('/add_reminder')}>+</a>
        <Reminder 
            subjectColor="blue"
            tagColor="red"
            tag="Important"
            date={(() => {
                const d = new Date();
                return(`${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`)
            })()}
            subjectName="Test"
            content="I hope this works :)"
            id={0}
        />
        <Reminders />
    </Base>
    </>;
}