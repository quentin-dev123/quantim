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
reminderArr = [];
tagArr = [];

reminderArr.forEach(function(element, index) {
	let reminder = document.createElement("div");
	reminder.class = "reminder";
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
			elemContent: element.tag
		},
		text: {
			htmlType: "p",
			elemContent: element.content
		}
	}; 
	Object.keys(myDict).forEach(function(element){
		let elem = document.createElement(elem_attributes.element.htmlType);
		elem.class = "reminder";
		elem.id = `rem${elem_attributes.element.htmlType}${index}`;
		document.getElementById(`remDiv${index}`).appendChild(elem);
	});
});
