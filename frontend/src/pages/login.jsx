import { useEffect } from "react";
import Form from "../components/form"
import { Password } from "../components/Password"
import { Username } from "../components/basic.form.components";

export default function Login(){
    return <>
    <Form title="Login" api_url="/api/login"> 
        <label htmlFor="username"><b> Entrer votre username </b></label>
        <Username />
        <label htmlFor="password"><b> Entrer votre mot de passe </b></label>
        <Password />
        <p>Vous n'avez pas de compte ? <a href="register">S'inscrire</a> </p>
        <a href="forgot_password">Mot de passe oublié</a>
    </Form>
    </>;
}