import React, { useRef, useEffect } from 'react';
import Tooltip from "../modules/tooltip.jsx";

function SchoolIcon(){
    let school_logo = {
        cursor: "pointer",
        border: "2px solid #f1f1f1",
        width: "54px",
        height: "54px",
        marginTop: "5px",
        marginBottom: "22px",
    }
    let link_div_style = {
        display: 'flex', 
        alignItems: 'center', 
        gap: '5px',
    }

    const link_div = useRef();

    useEffect(() => {
        // Adjust size of logo to match input height
        const logo = link_div.current.querySelector("img")
        const pronote_url = link_div.current.querySelector("input")
    
        logo.onclick = () => pronote_link("https://2160011n.index-education.net/pronote/eleve.html");
    }, []);
    
    function pronote_link(url){
        pronote_url.value = url
    }

    return (
        <div ref={link_div} style={link_div_style}>
            <Tooltip text="Appuyer seulement si vous êtes un élève au LFI de Hong Kong">
                <img 
                    id="lfi_logo" 
                    style={school_logo} 
                    src="/lfi_logo.png" 
                />
            </Tooltip>
            <input
                type="text"
                placeholder="Exemple: https://pronote.mon.ecole/eleve.html"
                name="pronote_url"
                autoComplete="pronote_url"
                required
            />
        </div>
    );
}

export { SchoolIcon };