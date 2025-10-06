import Form from "../components/form"
import { Input } from "../components/Inputs";

export default function Profile(){
    return <>
    <Form title="Profile" onSuccess={() => location.replace("/agenda")}>
        <label for="username"><b> Votre identifiant</b></label>
        <Input type="editable">
            <Input type="username" />
        </Input>
        <label for="email"><b> Votre adresse email </b></label>
        <Input type="editable">
            <Input type="email" />
        </Input>
        <label for="email"><b> Votre mot de passe </b></label>
        <Input type="editable">
            <Input type="password" />
        </Input>



        <input type="text" id="username" required disabled value="Loading..."/><i class="material-icons edit_icon" onclick="change_username('edit')" title="Modifier">&#xe254;</i><i class="material-icons check_icon hidden" onclick="change_username('save')" title="Modifier">check</i><i class="material-icons cross_icon hidden" onclick="change_username('cancel')" title="Annuler">clear</i>
        <label for="email"><b> Votre adresse email </b></label>
        <input type="email" id="email" required disabled value="Loading..."/>
        <label for="email"><b> Votre mot de passe </b></label>
        <input type="password" id="password" required disabled value="••••••••"/><i class="material-icons edit_icon" onclick="document.location='change_password'" title="Modifier">&#xe254;</i>

    </Form>
    </>;
}