import { useState, useRef } from "react";
import styles from "../style/form.module.css"
import { online } from "../modules/online.js";

function Password(){
    const [showPassword, setShowPassword] = useState(false);
    return <>
    <input
        type={showPassword ? "text" : "password"}
        placeholder="Mot de passe"
        name="password"
        autoComplete="current-password"
        pattern=".{4,}"
        title="Doit contenir au moins 4 caractères ou plus"
        required
    /><i
        className={`fa ${showPassword ? "fa-eye-slash" : "fa-eye"} ${styles.view_icon}`}
        title="Voir"
        onClick={() => setShowPassword((v) => !v)}
    ></i>  
    </>
}

function Username(){
    return<>
    <input type="text" placeholder="Username" name="username" autoComplete="username" required />
    </>
}

function Email(){
    return<>
    <input type="email" placeholder="Email" name="email" id="email" required />
    </>
}

function EditableInput(props){
    const input = props.children
    const containerRef = useRef(null);
    let previous_value = ""

    function toggle_icons() {
        if (containerRef.current) {
            const icons = containerRef.current.querySelectorAll('i');
            icons.forEach(icon => icon.classList.toggle('hidden'));
        }
    }

    function save_value(){
        if (!online()) return;
        if (input.value == previous_value){
            input.disabled = true
            toggle_icons()
        } else {
            return; // Do nothing for now
        }
    }

    function change_input(state){
        switch (state) {
            case "save":
                save_value()
                break;
            case "edit":
                toggle_icons()
                previous_value = input.value
                input.disabled = false
                input.focus()
                break;
            case "cancel":
                toggle_icons()
                input.value = previous_value
                input.disabled = true
                break;
        }
    }

    return (
        <div ref={containerRef}>
            {props.children}<i 
                className={`${styles.edit_icon} material-icons`}
                onClick={() => change_input('edit')}
                title="Modifier"
            >&#xe254;
            </i><i
                className={`${styles.check_icon} material-icons hidden`} 
                onClick={() => change_input('save')}
                title="Modifier"
            >check
            </i><i 
                className={`${styles.cross_icon} material-icons hidden`} 
                onClick={() => change_input('cancel')}
                title="Annuler"
            >clear
            </i>
        </div>
    )
}


function ReceiveEmailsCheckbox(){
    return<>
    <label htmlFor="accept_notif" style={{ cursor:"pointer"}}>
        <input type="checkbox"  name="accept_notif" id="accept_notif" style={{marginBottom:"15px", cursor:"pointer"}} defaultChecked /> J'accepte de recevoir des emails
    </label>
    </>
}

export function Input(props){
    switch (props.type){
        case "password": return <Password />
        case "username": return <Username />
        case "email": return <Email />
        case "editable": return <EditableInput>{props.children}</EditableInput>
        case "receive_emails": return <ReceiveEmailsCheckbox />
    }
}