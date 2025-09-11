import Form from "../components/form"
import { useEffect } from "react";

export default function Login(){
    useEffect(() => {
        alert("Login page rendered Successfully");
    }, []);
    return <>
    <Form title="Login"> 
        <label for="username"><b> Entrer votre username </b></label>
        <input type="text" placeholder="Username" name="username" autocomplete="username" required />
        <label for="password"><b> Entrer votre mot de passe </b></label>
        <input type="password" placeholder="Mot de passe" name="password" autocomplete="current-password" id="password1" required /><i class="fa fa-eye view_icon" id="view_icon1" onclick="toggle_password_visibility('1')"></i>
        {/*<p>Vous n'avez pas de compte ? <a href="register">S'inscrire</a> </p>
        <a href="forgot_password">Mot de passe oublié</a>*/}
    </Form>
    </>;
}