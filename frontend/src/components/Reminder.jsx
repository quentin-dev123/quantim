export default function Reminder(props){
    return <div style={{backgroundColor: props.subjectColor}}> 
        <span style={{backgroundColor: props.tagColor}}>{props.tag}</span>
        <span> {props.date}</span>

        <h2>{props.subject}</h2>

        <p>{props.content}</p>
    </div>
}