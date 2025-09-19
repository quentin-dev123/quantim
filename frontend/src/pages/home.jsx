import Base from "../components/base"
import styles from "../style/home.module.css"

export default function Home(){
    return <>
    <Base header="Accueil">
        <h1>Bienvenue</h1>
        <br></br>
        <a href="/login" className={styles.login}>Se connecter</a><br></br>
        <p>Vous n'avez pas de compte ?</p><a href="/register" className={styles.register}>S'inscrire</a>
    </Base>
    </>;
}