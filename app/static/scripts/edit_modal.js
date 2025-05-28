// Get the modal
var modal = document.getElementById('editmodal');
var reminder_id = undefined

var global_subject_id = 0
var global_tag_id = 0


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
    global_subject_id = subject.id
    subject_select.style.backgroundColor = subject.bg_color
    subject_select.style.color = "white";

    let tag = global_tagArr.find(myTag => myTag.id === reminder.tag_id);
    tag_select.value = tag.id
    global_tag_id = tag.id
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

const tag_modal = document.getElementById("editmodal_tag_modal")
const subject_modal = document.getElementById("editmodal_subject_modal")

const change_modal = document.getElementById("editmodal_change_modal")

function editmodal_close_a_modal (the_modal, selectId) {
    the_modal.style.display = "none";
    if (selectId){
        const select = document.getElementById(selectId)
        select.selectedIndex = "0";
      }
}

function removeAllEventListeners(element) {
    const clone = element.cloneNode(true);
    element.parentNode.replaceChild(clone, element);
    return clone;
  }
  
  function rgbToHex(rgb) {
    const rgbValues = rgb.substring(4, rgb.length - 1).split(',');
    return "#" + rgbValues.map(val => {
      const hex = parseInt(val).toString(16);
      return hex.length === 1 ? "0" + hex : hex;
    }).join('');
  }

  function hexToRgb(hex) {
    // Remove the '#' character if it exists
    hex = hex.replace("#", "");
  
    // Handle shorthand hex color codes (e.g., #abc)
    if (hex.length === 3) {
      hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    }
  
    // Parse the hex values for red, green, and blue
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);
  
    // Return the RGB color string
    return "rgb(" + r + ", " + g + ", " + b + ")";
  }


function open_change_modal(type){ // type = "subject" OR type = "tag"
    let h1 = change_modal.querySelector("label")
    let label = change_modal.querySelector("h1")
  
    let change_modal_name = change_modal.querySelector('input[type="text"]')
    let change_modal_bg_color = change_modal.querySelector('input[type="color"]')
  
    let option
    let id
    if (type == "subject"){
        h1.innerHTML = "<b>Matière</b>"
        label.innerHTML = "Changer une matière"
        option = subject_select.options[subject_select.selectedIndex];
        id = global_subject_id
    } else if (type == "tag") {
        h1.innerHTML = "<b>Tag</b>"
        label.innerHTML = "Changer un tag"
        option = tag_select.options[tag_select.selectedIndex];
        id = global_tag_id
    }
    change_modal.style.display = "block";
      
    change_modal_name.value = option.innerHTML;
    change_modal_bg_color.value = rgbToHex(option.style.backgroundColor);
  
    let change_modal_form = change_modal.querySelector("form")
    change_modal_form = removeAllEventListeners(change_modal_form);
    change_modal_form.addEventListener("submit", function(event){
      func_change_modal(type, id)
    });
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

function editmodal_changeSelect(elem, elemId) {
  switch (elem) {
            case "tag" :
                if (document.getElementById(elemId).value ===  "new") {
                  tag_modal.style.display = "block";
                }
                global_tag_id = document.getElementById(elemId).value;
                break;
            case "subject" :
                if (document.getElementById(elemId).value ===  "new") {
                  subject_modal.style.display = "block";
                }
                global_subject_id = document.getElementById(elemId).value;
                break;
        }
    const selectElement = document.getElementById(elemId)
    const selectedOption = selectElement.options[selectElement.selectedIndex]
    selectElement.style.backgroundColor = selectedOption.style.backgroundColor;
    selectElement.style.color = "white";
}

async function func_change_modal(type, id){ // type = "subject" OR type = "tag"
    event.preventDefault();  // Prevent the default form submission
  
  let subject_select = document.getElementById('editmodal_subject_select')
  let tag_select = document.getElementById('editmodal_tag_select')
  let select
  let post_link
  if (type == "subject"){
    select = subject_select
    post_link = `/api/subject/${id}`
  } else {
    select = tag_select
    post_link = `/api/tag/${id}`
  }

  option = select.options[select.selectedIndex];

  // Get elements
    const formElem = change_modal.querySelector("form")
    const formChildren = formElem.elements;
    const alertDiv = formElem.querySelector(".alert.alert-danger");
    const alertText = alertDiv.querySelector("span")
    const alertLink = alertDiv.querySelector("a");

    alertDiv.style.display = "none";

    const userAnswers = {};
    for (let i = 0; i < formChildren.length; i++) {
        if (["INPUT", "SELECT"].includes(formChildren[i].tagName)) {
            	userAnswers[formChildren[i].name] = formChildren[i].value;
        }
    }
    
    // Make a PUT request to the server
    let result = await fetch(post_link, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userAnswers)
    });
    if (result.ok) {
      
      let change_modal_name = change_modal.querySelector('input[type="text"]')
      let change_modal_bg_color = change_modal.querySelector('input[type="color"]')

      option.value = id;
      option.innerHTML = change_modal_name.value;

      const color = hexToRgb(change_modal_bg_color.value);
      option.style.backgroundColor = color;
      select.style.backgroundColor = color;
      document.getElementById("editmodal_change_name").innerHTML = "";

      editmodal_close_a_modal(change_modal, false)

    } else if (result.status === 400) {
        alertText.innerHTML = await result.text();
        alertDiv.style.display = "block";
    }

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
        editmodal_close_a_modal(modalElem, select_id)
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
