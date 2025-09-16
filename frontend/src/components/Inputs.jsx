import { useState } from "react";
import styles from "../style/form.module.css"

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

function ReceiveEmailsCheckbox(){
    return<>
    <label htmlFor="accept_notif" style={{ cursor:"pointer"}}>
        <input type="checkbox"  name="accept_notif" id="accept_notif" style={{marginBottom:"15px", cursor:"pointer"}} defaultChecked /> J'accepte de recevoir des emails
    </label>
    </>
}

function Input(props){
switch (props.type){
    case "password": return <Password />
    case "username": return <Username />
    case "email": return <Email />
    case "receive_emails": return <ReceiveEmailsCheckbox />
}
}
export { Input };