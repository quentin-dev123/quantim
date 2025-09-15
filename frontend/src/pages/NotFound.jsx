import { useImportCSS } from "../modules/modules.js";


export default function NotFound() {
    useImportCSS("./404.css");
    return <>
        <div className="container">
        <h1>404</h1>

        <p><strong>Page not found :(</strong></p>
        <p>The requested page could not be found.</p>
        <h2>To go back to the home page, click <a href="/">here</a></h2> 
        </div>
    </>;
}
