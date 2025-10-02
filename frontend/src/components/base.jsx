import "../style/base.css";
import "../style/tooltip.css";
import "../modules/tooltip.jsx";
import TopIcons from "./agenda_icons/topIcons.jsx";
import { Sidenav } from "./agenda_icons/sidenav.jsx";

export default function Base(props){
    return <>
        <header>
        <h1>{props.header}</h1>
        {props.topIcons && ( // Conditionally render the menuIcon
            <TopIcons />
        )}
        </header>
        <main>
            {props.children}
        </main>
            {props.afterContent}
        <footer>
        <p>&copy; <span id="date">2024-2025</span> <span /*onClick={openNav2()}*/>Quantim</span>. Tous droits réservés. 
        <br></br>
        <a href="/apidocs" className="white">API Docs</a>, <a href="/mention_legale.pdf" className="white">Mentions légales</a>, <a href="/politique_de_confidentialite.pdf" className="white">Politique de confidentialité</a>
        </p>
        </footer>
        <Sidenav />
    </>
}