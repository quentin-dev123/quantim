import { useEffect } from "react";
import "../style/home.page.css"
import Base from "../components/base"

export default function Home(){
    return <>
    <body>
    <Base header="Accueil">
        <h1>Bienvenue</h1>
        <br></br>
        <a href="/login" className="login">Se connecter</a><br></br>
        <p>Vous n'avez pas de compte ?</p><a href="/register" className="register">S'inscrire</a>
    </Base>
    </body>
    </>;
}