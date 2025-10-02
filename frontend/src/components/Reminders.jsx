import fetchReminders from "../modules/fetchReminders";
import Reminder from "./Reminder"
import { useState, useEffect } from "react";

function Reminders(){
    const [ reminders, setReminders ] = useState([])

    useEffect(() => {
        fetchReminders().then((r) => {
            if (!r[1]) {
                setReminders(r[0])
            } else {
                console.error("An error ocurred while fetching and/or parsing reminders");
                throw new Error(r[0])
            }
        })
    }, [])

    return (reminders.map((rem) => {
            console.log(rem)
            return (
        <Reminder 
                subjectColor={rem.subjectColor}
                tagColor={rem.tagColor}
                tag={rem.tag}
                date={rem.date}
                subjectName={rem.subject}
                content={rem.content}
                id={rem.id}
                key={rem.id}
            />);
        }))
}

export default Reminders;