import { useEffect } from "react";
import Base from "../components/base"
import { useImportCSS } from "../modules/modules.js";

export default function Home(){
    useImportCSS("./home.page.css");
    return <>
    <Base header="Accueil">
        <h1>Bienvenue</h1>
        <br></br>
        <a href="/login" className="login">Se connecter</a><br></br>
        <p>Vous n'avez pas de compte ?</p><a href="/register" className="register">S'inscrire</a>
    </Base>
    </>;
}