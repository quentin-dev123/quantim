import styles from "../../style/agenda_icons/sort_icon.module.css";
import { online } from "../../modules/online.js";
import Tooltip from "../../modules/tooltip.jsx";

function oc_dropdown() {
    const dropdown_content = document.getElementById('dropdown_content');
    const dropdown_content_hidden = dropdown_content.classList.contains('hide');
    if (!online() && dropdown_content_hidden) return;
    dropdown_content.classList.toggle('hide');
}

function close_dropdown() {
    const dropdown_content = document.getElementById('dropdown_content');
    dropdown_content.classList.add('hide');
}

function sort(type, event){
    event.stopPropagation();
    if (!online()) return;
    const date = document.getElementById('date_check')
    const matière = document.getElementById('matière_check')
    const tag = document.getElementById('tag_check')
    switch (type) {
        case 'date':
            //fetchData('/sort/date');
            date.classList.remove('hide')
            matière.classList.add('hide')
            tag.classList.add('hide')
            break;
        case 'matière':
            //fetchData('/sort/subject_id');
            date.classList.add('hide')
            matière.classList.remove('hide')
            tag.classList.add('hide')
            break;
        case 'tag':
            //fetchData('/sort/tag_id');
            date.classList.add('hide')
            matière.classList.add('hide')
            tag.classList.remove('hide')
            break;
    }
}

export default function SortIcon() {
    return (
        <div>
            <Tooltip text="Menu">
                <span 
                    className={`material-icons ${styles.icon}`}
                    id="sort_icon" 
                    onClick={oc_dropdown}
                >&#xe053;
                </span>
            </Tooltip>
            <div 
                className={`${styles.dropdown_content} hide`}
                id="dropdown_content"
            >
                <a 
                    onClick={(event) => sort('date', event)}
                >Date <i 
                        className={`fa-regular ${styles.check}`}
                        id="date_check"
                    >&#xf058;
                    </i>
                </a>
                <a 
                    onClick={(event) => sort('matière', event)}
                >Matière <i 
                        className={`fa-regular ${styles.check} hide`}
                        id="matière_check"
                    >&#xf058;
                    </i>
                </a>
                <a
                    onClick={(event) => sort('tag', event)}
                >Tag <i
                        className={`fa-regular ${styles.check} hide`} 
                        id="tag_check"
                    >&#xf058;
                    </i>
                </a>
            </div>
        </div>
    )
}