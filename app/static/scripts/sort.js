const sort_dropdown_content = document.getElementById('sort_icon-dropdown_content');
function sort_icon_dropdown_content(){
    event.stopPropagation()
    if (online()){
        close_filter_icon_dropdown_content()
        sort_dropdown_content.classList.toggle('show');
    }
}

function close_sort_icon_dropdown_content(){
    sort_dropdown_content.classList.remove('show');
}

// when the document is pressed
document.addEventListener('click', close_sort_icon_dropdown_content);

function sort(type, event){
event.stopPropagation();
const date = document.getElementById('sort_date_check')
const matière = document.getElementById('sort_matière_check')
const tag = document.getElementById('sort_tag_check')
if (type == 'date') {
    fetchData('/sort/date');
    date.classList.remove('hide')
    matière.classList.add('hide')
    tag.classList.add('hide')
}
else if (type == 'matière') {
    fetchData('/sort/subject_id');
    date.classList.add('hide')
    matière.classList.remove('hide')
    tag.classList.add('hide')
}
else if (type == 'tag') {
    fetchData('/sort/tag_id');
    date.classList.add('hide')
    matière.classList.add('hide')
    tag.classList.remove('hide')
}
}