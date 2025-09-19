import { useImportCSS, } from "../modules/modules.js";

function icons() {
    useImportCSS("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css");
    useImportCSS("https://fonts.googleapis.com/icon?family=Material+Icons");
}

function bootstrap() {
    useImportCSS("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css");
}

function fonts() {
    useImportCSS("https://fonts.googleapis.com/css?family=Anaheim");
    useImportCSS("https://fonts.googleapis.com/css?family=Architects%20Daughter");
}

export { icons, bootstrap, fonts };