import { useState, useEffect } from "react";
import Fetch from "./Fetch";

export default function fectReminders () {
// Need to add tag & subject fetch + treatment of asnwer

    const [[r, err], setResponse] = useState([null, false])

    useEffect(() => {
        Fetch("/api/reminder").then(([r, err]) => setResponse([r, err]));
    })

    useEffect(() => {
        if (r) {
            if (err) {
                alert("An error ocurred, please try again later");
                return [r, err];
            }
            return [r, err]
        }
    }, [r])

    return [r, err]
}