import { useState, useEffect } from "react";
import { Fetch, findInArray} from "./modules";


export default function fectReminders () {
// Need to add tag & subject fetch + treatment of asnwer

    const [[tags, tagErr], setTags] = useState([null, false])
    const [[subjects, subjectErr], setSubjects] = useState([null, false])
    const [[rems, remErr], setRems] = useState([null, false])
    const [jointArr, setJointArr] = useState(null)

    useEffect(() => {
        Fetch("/api/reminder").then(([r, err]) => jointArr += [r, err]);
        Fetch("/api/tag").then(([r, err]) => jointArr += [r, err]);
        Fetch("/api/subject").then(([r, err]) => jointArr += [r, err]);
    })

    useEffect(() => {
        if (jointArr.length === 3) {
            const err = findInArray(jointArr, 1, true);
            if (err) {
                return [err[0], err[1]]
            }
            
        }
    }, [tags, subjects, rems, finalArr])

    return [r, err]
}