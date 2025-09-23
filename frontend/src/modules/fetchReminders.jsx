import { useEffect } from "react";
import { Fetch, findInArray} from "./modules";


export default function fetchReminders () {
// Need to add tag & subject fetch + treatment of asnwer

    useEffect(() => {
        Promise.all([Fetch({url:"/api/reminder"}), Fetch({url: "/api/tag"}), Fetch({url: "/api/subject"})])
        .then((res) => {
            treatRems(res);
        })
    }, [])

    function treatRems (jointArr) {
        if (jointArr.length === 3) {
            const err = findInArray(jointArr, 1, true);
            if (err) {
                return [err[0], err[1]]
            }
            var final = []
            var subjects = {}
            var tags = {}
            for (let i = 0; i < jointArr[0][0].length; i++) {
                const rem = jointArr[0][0][i]
                if (!tags[rem.tagId]) {
                    tags += findInArray(jointArr[1][0], id, rem.tagId)
                }
                const tag = tags[rem.tagId]
                if (!subjects[rem.subjectId]) {
                    subjects += findInArray(jointArr[2][0], id, rem.subjectId)
                }
                const subject = subjects[rem.subjectId]
                const finalRem = {
                    date: rem.date,
                    content: rem.content,
                    id: rem.id,
                    subject: subject.content,
                    subjectColor: subject.color,
                    tag: tag.content,
                    tagColor: tag.color
                }
                final += finalRem;
            }
            return [final, false]
        }
    }
}