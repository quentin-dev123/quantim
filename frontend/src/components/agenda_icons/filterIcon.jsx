import styles from "../../style/agenda_icons/filter_icon.module.css";
import { online } from "../../modules/online.js";
import Tooltip from "../../modules/tooltip.jsx";


function oc_dropdown() {
    const dropdown_content = document.getElementById('dropdown_content');
    const dropdown_content_hidden = dropdown_content.classList.contains('hide');
    if (!online() && dropdown_content_hidden) return;
    dropdown_content.classList.toggle('hide');
}

function close_dropdown(){
    const dropdown_content = document.getElementById('dropdown_content');
    dropdown_content.classList.add('hide');
}









function filter(event){
    event.stopPropagation();

    const target = event.target; // Get the clicked button
    const type = target.id; // Get the button id which corresponds to the type
    const buttonContainer = document.querySelector(styles.display_flex); // Get the container div

    // Remove 'on' class from all buttons and 'hidden' from all containers
    buttonContainer.querySelectorAll('*').forEach(button => button.classList.remove('on'));
    document.querySelectorAll(styles.my_container).forEach(container => container.classList.add('hidden'));

    // Add 'on' class to the selected button and remove 'hidden' from the corresponding container
    target.classList.add(styles.on);
    document.getElementById(`${type}_container`).classList.remove('hidden');
}



function SelectContainer(name, fname, hidden=true){
    // Same divs and same select as editmodal
    return (
        <div className={`${styles.my_container} ${hidden ? 'hide' : ''}`} id={`${name}_container`}>
            <div className={styles.select_container}>
                <select className={styles.form_select} onChange={(e) => changeSelect(name, e)} required>
                    <option className="bgwhite_cblack" value="reset" defaultValue>Réinitialiser</option>
                    <optgroup className="hide" label={fname}>
                    </optgroup>
                </select>
            </div>
        </div>
    )
}

export default function FilterIcon() {
    return (
        <div>
            <Tooltip text="Filtrer" left={true} >
                <span className={`fas ${styles.icon}`} id="filter_icon" onClick={oc_dropdown}>&#xf0b0;</span>
            </Tooltip>
            <div className={`${ styles.dropdown_content} hide`} id="dropdown_content" onClick={(e) => e.stopPropagation()}>
                <div className={styles.display_flex}>
                    <a onClick={(e) => filter(e)} id="subject" className={styles.on}>Matière</a>
                    <a onClick={(e) => filter(e)} id="tag">Tag</a>
                    <a onClick={(e) => filter(e)} id="date" className="hide">Date</a>
                </div>

                <SelectContainer name="subject" fname="Matière" hidden={false} />
                <SelectContainer name="tag" fname="Tag" />
                <div className={`${styles.my_container} hide`} id="date_container">
                    <div className={styles.select_container}>
                        <input className={styles.form_date} type="date" name="date" onChange={(event) => changeDate(event)} required />
                    </div>
                </div>
            </div>
        </div>
    )
}