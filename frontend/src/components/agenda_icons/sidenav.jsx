import styles from "../../style/sidenav.module.css"
import { online } from "../../modules/online.js";
import Tooltip from "../../modules/tooltip.jsx";

function setNavWidth(width) {
    document.getElementById("mySidenav").style.width = width;
}
function openNav() {
    setNavWidth("250px");
}
function closeNav() {
    setNavWidth("0");
    closeAmerlioration();
}


function toggleAmelioration(){
  const amelioration_a = document.getElementById("amelioration_a")
  const amelioration_div = document.getElementById("amelioration_div")
  if (online) {
    amelioration_div.classList.toggle('hide')
    amelioration_a.classList.toggle(styles.on)
  }
}
function closeAmerlioration(){
    amelioration_div.classList.add('hide')
    amelioration_a.classList.remove(styles.on)
}


export function MenuIcon() {
    return (
        <Tooltip text="Menu">
            <span className={styles.menu_icon} onClick={openNav}>&#9776;</span>
        </Tooltip>
    )
}


export function Sidenav() {
    return (
        <div id="mySidenav" className={styles.sidenav}>
            <a className={styles.closebtn} onClick={closeNav}>&times;</a>
            <a href="/">Accueil</a>
            <a href="/profile" className={styles.blue}>Votre profile</a>
            <a href="/logout">Se déconnecter</a>
            <a onClick={toggleAmelioration} id="amelioration_a">Proposer une amélioration</a>
            <div className={`${styles.amelioration} hide`} id="amelioration_div">
                <form>
                    <textarea rows="5" required></textarea>
                    <label>
                        <input type="checkbox" required /> Anonyme
                    </label>
                    <div>
                        <button type="button" onClick={toggleAmelioration}>Annuler</button>
                        <button type="submit">Envoyer</button>
                    </div>
                </form>
            </div>
            <a href="/fetch_from_pronote" className={styles.green}>Se connecter à Pronote</a>
        </div>
    );
}