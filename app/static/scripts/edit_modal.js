// Get the modal
var modal = document.getElementById('editmodal');
var reminder_id = undefined

function editmodal_close_modal() {
    modal.classList.add("hidden");
}

function editmodal_open_modal(id) {
    modal.classList.remove("hidden");
    fetchReminder(id)
    reminder_id = id
    console.log(id)
}

const datePicker = document.getElementById("editmodal_datePicker");
const content = document.getElementById('editmodal_Contenu');
const subject_select = document.getElementById('editmodal_subject_select');
const tag_select = document.getElementById('editmodal_tag_select')

datePicker.min = new Date().toISOString().split("T")[0];

async function fetchReminder (id) { 
    let reminder = await (await fetch("/api/reminder/" + id)).json();

    datePicker.value = reminder.date.split("T")[0]
    content.value = reminder.content

    let subject = global_subjectArr.find(mySubject => mySubject.id === reminder.subject_id);
    subject_select.value = subject.id
    subject_select.style.backgroundColor = subject.bg_color
    subject_select.style.color = "white";

    let tag = global_tagArr.find(myTag => myTag.id === reminder.tag_id);
    tag_select.value = tag.id
    tag_select.style.backgroundColor = tag.bg_color
    tag_select.style.color = "white";

}

const form = document.getElementById("editmodal_form");
form.addEventListener('submit',  async (event) => {
    event.preventDefault();  // Prevent the default form submission

    // Get elements
    const formChildren = form.elements;
    const alertDiv = document.getElementById("editmodal_alert")
    const alertText = document.getElementById("editmodal_alert_text");
    const alertLink = document.getElementById("editmodal_alert_link");

    alertDiv.style.display = "none";

    const userAnswers = {};
    for (let i = 0; i < formChildren.length; i++) {
        if (["INPUT", "SELECT"].includes(formChildren[i].tagName)) {
          if (formChildren[i].type === "checkbox") {
            userAnswers[formChildren[i].name] = formChildren[i].checked;
          } else {
            	userAnswers[formChildren[i].name] = formChildren[i].value;
          }
        }
    }

    // Make a PUT request to the server
    const reminder_id = window.reminder_id; // Access the reminder_id variable from the window object
    let result = await fetch("/api/reminder/" + reminder_id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userAnswers)
    });
    if (result.ok) {
        window.location.reload(true);
    } else if (result.status === 400) {
        const response = await result.json();
        alertText.innerHTML = response["message"];
        if (response["link_display"]) {
            alertLink.innerHTML = response["link_display"];
            alertLink.href = response["link_href"];
        } else {
            alertLink.innerHTML = "";
        }
        alertDiv.style.display = "block";
    }
});








// Show icons functions
// does not work as editmodal_icon_subject and editmodal_icon_tag classes do not exist
function show_icons_subject(){
	let icons = document.getElementsByClassName("editmodal_icon_subject");
    for (let i = 0; i < icons.length; i++) {
        icons[i].style.display = "block";
    }
}

function show_icons_tag(){
	let icons = document.getElementsByClassName("editmodal_icon_tag");
    for (let i = 0; i < icons.length; i++) {
    	icons[i].style.display = "block";
	}
}


function findIndexfromOptionName( select, optionName ) {
    let options = Array.from( select.options );
    return options.findIndex( (opt) => opt.value == optionName );
}

function close_a_modal (the_modal, selectId) {
    the_modal.style.display = "none";
    const select = document.getElementById(selectId)
    select.selectedIndex = "0";
}

async function dynamic_options(fetch_route, optgroup_id){
    let optionGroup = document.getElementById(optgroup_id);
    let result = await fetch(fetch_route)
    const response = await result.json();
    if (response !== "") {
        response.forEach(element => {
            let option = document.createElement("option");
            option.value = element.id;
            option.innerHTML = element.content;
            option.style.backgroundColor = element.bg_color;
            option.style.color = 'white';
            optionGroup.appendChild(option);
        });
        optionGroup.style.display = "block";
    }
};

dynamic_options("/api/tag", "editmodal_optionGroup2");
dynamic_options("/api/subject", "editmodal_optionGroup");

const tag_modal = document.getElementById("editmodal_tag_modal")
const subject_modal = document.getElementById("editmodal_subject_modal")

function editmodal_changeSelect(elem, elemId) {
    if (document.getElementById(elemId).value ===  "new") {
        switch (elem) {
            case "tag" :
                tag_modal.style.display = "block";
                break;
            case "subject" :
                subject_modal.style.display = "block";
                break;
        }
    }
    const selectElement = document.getElementById(elemId)
    const selectedOption = selectElement.options[selectElement.selectedIndex]
    selectElement.style.backgroundColor = selectedOption.style.backgroundColor;
    selectElement.style.color = "white";
}

async function secondary_modal(event, post_link, modalElem, select_id) {
    event.preventDefault();  // Prevent the default form submission

    // Get elements
    const formElem = modalElem.querySelector("form")
    const formChildren = formElem.elements;
    const alertDiv = formElem.querySelector(".edit_alert.edit_alert-danger");
    const alertText = alertDiv.querySelector("span")
    const alertLink = alertDiv.querySelector("a");

    alertDiv.style.display = "none";

    const userAnswers = {};
    for (let i = 0; i < formChildren.length; i++) {
        if (["INPUT", "SELECT"].includes(formChildren[i].tagName)) {
            	userAnswers[formChildren[i].name] = formChildren[i].value;
        }
    }

    // Make a POST request to the server
    let result = await fetch(post_link, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userAnswers)
    });
    if (result.ok) {
        const response = await result.json();
        let selectElem = document.getElementById(select_id);
        let optionGroup = selectElem.querySelector('optgroup');
        let option = document.createElement("option");
        option.value = response.id;
        option.innerHTML = response.content;
        option.style.backgroundColor = response.bg_color;
        option.style.color = 'white';
        selectElem.style.backgroundColor = response.bg_color;
        selectElem.style.color = 'white';
        optionGroup.appendChild(option);
        close_a_modal(modalElem, select_id)
        let created_index = findIndexfromOptionName(selectElem, option.value)
        selectElem.selectedIndex = created_index;
    } else if (result.status === 400) {
        alertText.innerHTML = await result.text();
        alertDiv.style.display = "block";
    }
}

tag_modal.querySelector("form").addEventListener("submit", function(event){
    secondary_modal(event, "/api/tag", tag_modal, "editmodal_tag_select");
    document.getElementById("editmodal_Nom_tag").innerHTML = "";
});
subject_modal.querySelector("form").addEventListener("submit", function(event){
    secondary_modal(event, "/api/subject", subject_modal, "editmodal_subject_select");
    document.getElementById("editmodal_Nom_subject").innerHTML = "";
});
