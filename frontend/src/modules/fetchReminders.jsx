import { useState, useEffect } from "react";
import { Fetch, findInArray} from "./modules";


export default function fectReminders () {
// Need to add tag & subject fetch + treatment of asnwer
    const [jointArr, setJointArr] = useState(null)

    useEffect(() => {
        Promise.all([Fetch("/api/reminder"), Fetch("/api/tag"), Fetch("/api/subject")])
        .then((res) => {
            setJointArr(res);
        })
    })

    useEffect(() => {
        if (jointArr.length === 3) {
            const err = findInArray(jointArr, 1, true);
            if (err) {
                return [err[0], err[1]]
            }
            var subjects = {}
            for (let i = 0; i < jointArr[0][0].length; i++) {
                const rem = jointArr[0][0][i]
                const tag = jointArr[1][0][i]
                if (!subjects[rem.subjectId]) {
                    subjects += findInArray(jointArr[2][0], id, rem.subjectId)
                }
                const subject = subjects[rem.subjectId] ? subjects[rem.subjectId] : findInArray(jointArr[2][0], id, rem.subjectId)
                const finalRem = {
                    date: rem.date,
                    content: rem.content,
                    id: rem.id,
                    subjectName: 
                }
            }
        }
    }, [jointArr])

    return [r, err]
}