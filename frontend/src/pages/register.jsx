import Form from "../components/form"
import { Input } from "../components/Inputs"

export default function Register(){
    return <>
    <Form title="S'inscrire" api_url="/register"> 
        <label htmlFor="username"><b> Choisissez un identifiant</b></label>
        <Input type="username" />
        <label htmlFor="email"><b> Entrer votre adresse email </b></label>
        <Input type="email" />
        <label htmlFor="password1"><b> Choisissez un mot de passe </b></label>
        <Input type="password" />
        <label htmlFor="password2"><b> Confirmez votre mot de passe </b></label>
        <Input type="password" />
        <Input type="receive-emails" />
    </Form>
    </>;
}