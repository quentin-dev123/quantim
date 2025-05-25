const filter_datePicker = document.getElementById("filter_datePicker");
filter_datePicker.min = new Date().toISOString().split("T")[0];

const filter_dropdown_content = document.getElementById('filter_dropdown_content');
    function filter_icon_dropdown_content(){
        event.stopPropagation()
        close_sort_icon_dropdown_content()
        filter_dropdown_content.classList.toggle('hide');
    }

    function close_filter_icon_dropdown_content(){
        filter_dropdown_content.classList.add('hide');
    }

    // when the document is pressed
    document.addEventListener('click', close_filter_icon_dropdown_content);

  function filter(type, event){
    event.stopPropagation();
    const subject = document.getElementById('filter_matière')
    const tag = document.getElementById('filter_tag')
    const date = document.getElementById('filter_date')
    const subjectContainer = document.getElementById("subject_container")
    const tagContainer = document.getElementById("tag_container")
    const dateContainer = document.getElementById("date_container")
    if (type == 'subject') {
      subject.classList.add('on')
      tag.classList.remove('on')
      date.classList.remove('on')
      subjectContainer.classList.remove('hidden')
      tagContainer.classList.add('hidden')
      dateContainer.classList.add('hidden')
    }
    else if (type == 'tag') {
      subject.classList.remove('on')
      tag.classList.add('on')
      date.classList.remove('on')
      subjectContainer.classList.add('hidden')
      tagContainer.classList.remove('hidden')
      dateContainer.classList.add('hidden')
    }
    else if (type == 'date') {
      subject.classList.remove('on')
      tag.classList.remove('on')
      date.classList.add('on')
      subjectContainer.classList.add('hidden')
      tagContainer.classList.add('hidden')
      dateContainer.classList.remove('hidden')
    }
  }

  async function filter_dynamic_options(fetch_route, optgroup_id){
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

  filter_dynamic_options("/api/subject", "filter_subject_optionGroup");
  filter_dynamic_options("/api/tag", "filter_tag_optionGroup");


  function filter_reset_select(elem_id){
    let elem = document.getElementById(elem_id)
    elem.value = "reset"
    elem.style.backgroundColor = "white";
    elem.style.color = "black";
  }
  
  function filter_changeSelect(elem, event){
    event.stopPropagation()
    const selectElement = document.getElementById(`filter_${elem}_select`)
    const selectedOption = selectElement.options[selectElement.selectedIndex]
    const optionValue = selectedOption.value
    if (elem == "subject"){
        filter_reset_select("filter_tag_select")
    } 
    else if (elem == "tag"){
        filter_reset_select("filter_subject_select")
    }

    if (optionValue == "reset"){
        fetchData("");
    }
    else {
        fetchData(`/filter/${elem}_id/${optionValue}`);
    }

    selectElement.style.backgroundColor = selectedOption.style.backgroundColor;
    selectElement.style.color = selectedOption.style.color;
  }


  function filter_changeDate(event){
    event.stopPropagation()
    filter_reset_select("filter_tag_select")
    filter_reset_select("filter_subject_select")

    const dateValue = filter_datePicker.value
    fetchData(`/filter/date/${dateValue}`)
  }



  function stopPropagation(event){
    event.stopPropagation()
  }