import Form from "../components/form"
import { Input } from "../components/Inputs";
import { SchoolIcon } from "../components/school_icon";

export default function LoginPronote(){
    return <>
    <Form title="Récuperer vos devoirs de PRONOTE" api_url="/api/login" onSuccess={() => location.replace("/")}> { /* Need to change to /agenda once it exists*/}
        <label htmlFor="pronote_url"><b> Entrer le lien que vous utilisez pour accéder à PRONOTE</b></label>
            <SchoolIcon />
        <label htmlFor="username"><b> Entrer votre identifiant PRONOTE</b></label>
        <Input type="username" />
        <label htmlFor="password"><b> Entrer votre mot de passe PRONOTE</b></label>
        <Input type="password" />
    </Form>
    </>;
}