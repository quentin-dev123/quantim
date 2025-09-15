import { useState } from "react";
import style from "../style/form.module.css"

function Password(){
    const [showPassword, setShowPassword] = useState(false);
    return <>
    <input
        type={showPassword ? "text" : "password"}
        placeholder="Mot de passe"
        name="password"
        autoComplete="current-password"
        required
    /><i
        className={`fa ${showPassword ? "fa-eye-slash" : "fa-eye"} ${style.view_icon}`}
        title="Voir"
        onClick={() => setShowPassword((v) => !v)}
    ></i>
    </>
}

function NewPassword(){
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
        className={`fa ${showPassword ? "fa-eye-slash" : "fa-eye"} ${style.view_icon}`}
        title="Voir"
        onClick={() => setShowPassword((v) => !v)}
    ></i>  
    </>
}

export { Password, NewPassword }