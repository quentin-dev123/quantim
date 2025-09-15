import { useEffect } from "react";
import Form from "../components/form"
import { Password, NewPassword } from "../components/Password"
import { Username, Email, ReceiveEmailsCheckbox } from "../components/basic.form.components"

export default function Register(){
    return <>
    <Form title="S'inscrire" api_url="/register"> 
        <label htmlFor="username"><b> Choisissez un identifiant</b></label>
        <Username />
        <label htmlFor="email"><b> Entrer votre adresse email </b></label>
        <Email />
        <label htmlFor="password1"><b> Choisissez un mot de passe </b></label>
        <NewPassword />
        <label htmlFor="password2"><b> Confirmez votre mot de passe </b></label>
        <Password />
        <ReceiveEmailsCheckbox />
    </Form>
    </>;
}