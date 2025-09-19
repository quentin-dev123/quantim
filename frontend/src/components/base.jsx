import "../style/base.css";
import "../style/tooltip.css";

export default function Base(props){
    return <>
        <header>
        <h1>{props.header}</h1>
        {props.menuIcon}
        </header>
        <main>
            {props.children}
        </main>
            {props.afterContent}
        <footer>
        <p>&copy; <span id="date">2024-2025</span> <span /*onClick={openNav2()}*/>Quantim</span>. Tous droits réservés. 
        <br></br>
        <a href="/apidocs" className="white">API Docs</a>, <a href="/static/mention_legale.pdf" className="white">Mentions légales</a>, <a href="/static/politique_de_confidentialite.pdf" className="white">Politique de confidentialité</a>
        </p>
        </footer>
    </>
}