import { useImportCSS } from "../modules/modules.js";

function startRedirect() {
    window.location.href = "/home";
}

export default function NotFound() {
    useImportCSS("./404.css");
    return <>
        <div className="container">
        <h1>404</h1>

        <p><strong>Page not found :(</strong></p>
        <p>The requested page could not be found.</p>
        <div onLoad={startRedirect()}> <h2>If you are not redirected shortly, please click <a href="/home">here</a></h2> </div>
        </div>
    </>;
}
