import Form from "../components/form"
import Password from "../components/Password"
import { useEffect } from "react";

export default function Login(){
    return <>
    <Form title="Login"> 
        <label htmlFor="username"><b> Entrer votre username </b></label>
        <input type="text" placeholder="Username" name="username" autoComplete="username" required />
        <label htmlFor="password"><b> Entrer votre mot de passe </b></label>
        <Password />
        {/*<p>Vous n'avez pas de compte ? <a href="register">S'inscrire</a> </p>
        <a href="forgot_password">Mot de passe oublié</a>*/}
    </Form>
    </>;
}