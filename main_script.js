function adjustColorBrightness(color, percent) {
    let num = parseInt(color.slice(1), 16);
    let amt = Math.round(2.55 * percent);
    let r = (num >> 16) + amt;
    let g = (num >> 8 & 0x00FF) + amt;
    let b = (num & 0x0000FF) + amt;

    r = Math.max(0, Math.min(255, r));
    g = Math.max(0, Math.min(255, g));
    b = Math.max(0, Math.min(255, b));

    return `#${(r << 16 | g << 8 | b).toString(16).padStart(6, '0')}`;
}

class myReminderClass {
    constructor (content, subject, tag, date) {
        this.content = content;
        this.subject = subject; // Corrected
        this.tag = tag;
        this.date = date;
    }
}
class tag {
    constructor (content, bgColor) {
        this.content = content;
        this.bgColor = bgColor;
    }
}
class mySubjectClass {
	constructor (name, bgColor) {
        this.name = name;
        this.bgColor = bgColor;
    }
}

const tagArr = {
    test: new tag("Urgent", "red")
};
const subjectArr = {
	testing: new mySubjectClass("Coding", "blue")
};

const reminderArr = [
    new myReminderClass(
        "Finir de développer ce site !",
        subjectArr.testing,
        tagArr.test,
        new Date("2024-01-25")
    )
];

reminderArr.forEach(function(element, index) {
    let reminder = document.createElement("div");
    reminder.className = "reminder-container"; // Renamed for clarity
    reminder.style.backgroundColor = element.subject.bgColor; // Corrected typo
    reminder.id = `remDiv${index}`;
    document.body.appendChild(reminder);
    const elem_attributes = {
        tagged: {
            htmlType: "a",
            elemContent: element.tag.content,
            elemBgColor: element.tag.bgColor
        },
        date: {
            htmlType: "h3",
            elemContent: "For : " + element.date.toLocaleDateString('en-GB')
        },
        topic: {
            htmlType: "h2",
            elemContent: element.subject.name // Corrected to display subject name
        },
        text: {
            htmlType: "p",
            elemContent: element.content
        }
    }; 
    Object.keys(elem_attributes).forEach(function(attr){
        let elem = document.createElement(elem_attributes[attr].htmlType);
        elem.innerHTML = elem_attributes[attr].elemContent;
        elem.className =  `reminder${elem_attributes[attr].htmlType}`; // Made class more specific
        elem.id = `rem${elem_attributes[attr].htmlType}${index}`;
        if (elem_attributes[attr].htmlType === "a") {
            elem.style.backgroundColor = elem_attributes[attr].elemBgColor;
        }
        document.getElementById(`remDiv${index}`).appendChild(elem);
    });
});
