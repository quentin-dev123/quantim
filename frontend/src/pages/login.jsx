import Form from "../components/form"
import { Input } from "../components/Inputs";

export default function Login(){
    return <>
    <Form title="Login" api_url="/api/login"> 
        <label htmlFor="username"><b> Entrer votre username </b></label>
        <Input type="username" />
        <label htmlFor="password"><b> Entrer votre mot de passe </b></label>
        <Input type="password" />
        <p>Vous n'avez pas de compte ? <a href="register">S'inscrire</a> </p>
        <a href="forgot_password">Mot de passe oublié</a>
    </Form>
    </>;
}