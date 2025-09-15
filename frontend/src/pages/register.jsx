import { useEffect } from "react";
import Form from "../components/form"
import { Password, NewPassword } from "../components/Password"

export default function Register(){
    return <>
    <Form title="S'inscrire" api_url="/register"> 
        <label htmlFor="username"><b> Choisissez un identifiant</b></label>
        <input type="text" placeholder="Username" name="username" id="username" required />
        <label htmlFor="email"><b> Entrer votre adresse email </b></label>
        <input type="email" placeholder="Email" name="email" id="email" required />
        <label htmlFor="password1"><b> Choisissez un mot de passe </b></label>
        <NewPassword />
        <label htmlFor="password2"><b> Confirmez votre mot de passe </b></label>
        <Password />
        <label htmlFor="accept_notif" style={{ cursor:"pointer"}}>
            <input type="checkbox"  name="accept_notif" id="accept_notif" style={{marginBottom:"15px", cursor:"pointer"}} defaultChecked /> J'accepte de recevoir des emails
        </label>
    </Form>
    </>;
}