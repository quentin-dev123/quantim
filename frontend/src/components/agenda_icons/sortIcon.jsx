import styles from "../../style/agenda_icons.module.css";
import { online } from "../../modules/online.js";
import Tooltip from "../../modules/tooltip.jsx";

function open_dropdown_content() {
    if (!online()) return;
    const sort_dropdown_content = document.getElementById('sort_icon-dropdown_content');
    sort_dropdown_content.classList.toggle('hide');
}

function close_dropdown_content() {
    const sort_dropdown_content = document.getElementById('sort_icon-dropdown_content');
    sort_dropdown_content.classList.remove('hide');
}

function sort(type, event){
    event.stopPropagation();
    if (!online()) return;
    const date = document.getElementById('sort_date_check')
    const matière = document.getElementById('sort_matière_check')
    const tag = document.getElementById('sort_tag_check')
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
                    className={`material-icons ${styles.sort_icon}`}
                    id="sort_icon" 
                    onClick={open_dropdown_content}
                >&#xe053;
                </span>
            </Tooltip>
            <div 
                className={` ${styles.sort_icon_dropdown_content} hide`}
                id="sort_icon-dropdown_content"
            >
                <a 
                    onClick={(event) => sort('date', event)}
                >Date 
                    <i 
                        className={`fa-regular ${styles.check}`}
                        id="sort_date_check"
                    >&#xf058;
                    </i>
                </a>
                <a 
                    onClick={(event) => sort('matière', event)}
                >Matière 
                    <i 
                        className={`fa-regular ${styles.check} hide`}
                        id="sort_matière_check"
                    >&#xf058;
                    </i>
                </a>
                <a
                    onClick={(event) => sort('tag', event)}
                >Tag
                    <i
                        className={`fa-regular ${styles.check} hide`} 
                        id="sort_tag_check"
                    >&#xf058;
                    </i>
                </a>
            </div>
        </div>
    )
}