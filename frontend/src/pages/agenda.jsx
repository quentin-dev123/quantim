import Base from "../components/base"
import Reminder from "../components/Reminder";
import Reminders from "../components/Reminders";

export default function Agenda(){
    return <>
    <Base header="Agenda">
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
    />
    <Reminders />
    </Base>
    </>;
}