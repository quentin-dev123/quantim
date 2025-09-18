import React, { useRef, useEffect } from 'react';

function SchoolIcon(){
    let school_logo = {
    cursor: "pointer",
    border: "2px solid #f1f1f1",
    width: "30px",
    height: "30px",
    }

    const link_div = useRef();

    useEffect(() => {
        // Adjust size of logo to match input height
        const tooltip_container = link_div.current.querySelector("div")
        const logo = link_div.current.querySelector("img")
        const pronote_url = link_div.current.querySelector("input")

        let logo_height = pronote_url.offsetHeight + 'px';
        logo.style.height = logo_height;
        logo.style.width = logo_height;
        tooltip_container.style.width = logo_height;
        pronote_url.style.width = pronote_url.offsetWidth - pronote_url.offsetHeight - 5 + 'px';
    
        logo.onclick = () => pronote_link("https://2160011n.index-education.net/pronote/eleve.html");
    }, []);
    
    function pronote_link(url){
        pronote_url.value = url
    }

    return <>
    <div ref={link_div}>
        <div className="tooltip_container" style={{display: "inline-block"}}>
            <img id="lfi_logo" style={school_logo} src="/lfi_logo.png" />
            <label className="tooltip">Appuyer seulement si vous êtes un élève au LFI de Hong Kong</label>
        </div>
        <input id="pronote_url" type="text" placeholder="Exemple: https://pronote.mon.ecole/eleve.html" name="pronote_url" autoComplete="pronote_url" required />
    </div>
    </>
}

export { SchoolIcon };