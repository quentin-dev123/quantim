import { useState } from "react";
import style from "../style/form.module.css"

export default function Password(){
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
        onClick={() => setShowPassword((v) => !v)}
    ></i>
    </>
}