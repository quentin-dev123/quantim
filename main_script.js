class myReminderClass {
	constructor (content, name, subject, tag) {
		this.content = content;
		this.name = name;
		this.subject = subject;
		this.tag = tag;
	}
}
class tag {
	constructor (content, bgColor) {
		this.content = content;
		this.bgColor = bgColor;
	}
}
reminderArr = [
	new myReminderClass(
      "As you can see, this is a test",
      "A test",
      "Testing",
      "Tests"
    )
];
tagArr = [];

reminderArr.forEach(function(element, index) {
	let reminder = document.createElement("div");
	reminder.className = "reminder";
	reminder.id = `remDiv${index}`;
	document.body.appendChild(reminder);
	const elem_attributes = {
		title: {
			htmlType: "h3",
			elemContent: element.name
		},
		topic: {
			htmlType: "h4",
			elemContent: element.subject
		},
		tagged: {
			htmlType: "a",
			elemContent: element.tag.content,
            elemBgColor: element.tag.bgColor
		},
		text: {
			htmlType: "p",
			elemContent: element.content
		}
	}; 
	Object.keys(elem_attributes).forEach(function(element){
		let elem = document.createElement(elem_attributes.element.htmlType);
        elem.innerHTML = elem_attributes.element.elemContent;
		elem.className = "reminder";
		elem.id = `rem${elem_attributes.element.htmlType}${index}`;
        if (elem_attributes.element.htmlType === "a") {
        	elem.style.background-color = elem_attributes.element.elemBgColor;
        }
		document.getElementById(`remDiv${index}`).appendChild(elem);
	});
});
