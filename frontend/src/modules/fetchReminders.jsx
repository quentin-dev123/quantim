import { useEffect } from "react";
import { Fetch, findInArray} from "./modules";


export default async function fetchReminders () {
// Need to add tag & subject fetch + treatment of asnwer

    var reminders = await Fetch({url:"/api/reminder"});
    var tags = await Fetch({url: "/api/tag"});
    var subjects = await Fetch({url: "/api/subject"})
    var arr = [reminders, tags, subjects]

    const err = findInArray(arr, 1, true);
    if (err) {
        console.error("An error ocurred while fetching reminders and/or tags and/or subjects")
        return [err[0], true]
    }

    var final = []
    var parsed_tags= {}
    var parsed_subjects= {}

    for (let i = 0; i < reminders[0].length; i++) {
        const rem = reminders[0][i]
        if (!parsed_tags[rem["tag_id"]]) {
            parsed_tags[rem.tag_id] = findInArray(tags[0], "id", rem["tag_id"])
        }
        const tag = parsed_tags[rem["tag_id"]]
        if (!parsed_subjects[rem.subjectId]) {
            parsed_subjects[rem["subject_id"]] = findInArray(subjects[0], "id", rem["subject_id"])
        }
        const subject = parsed_subjects[rem["subject_id"]]
        const finalRem = {
            date: rem.date,
            content: rem.content,
            id: rem.id,
            subject: subject.content,
            subjectColor: subject.bg_color,
            tag: tag.content,
            tagColor: tag.bg_color
        }
        final.push(finalRem);
    }
    return [final, false]
}