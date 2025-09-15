import { useState, useEffect } from "react";
import { useFetch } from "../modules/modules.js";
import { icons, bootstrap, tooltip } from "../modules/stylesheets.js";
import { useImportCSS } from "../modules/modules.js";

export default function Form(props){
    useImportCSS("./form.module.css");
    icons(); bootstrap(); tooltip();
    const [fetchParams, setFetchParams] = useState(false);
    const [response, error] = useFetch(fetchParams || {});

    useEffect(() => {console.log(error.err ? error.msg : "success (for now)")}, [error])

    const submit_form = (event) => {
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);
      const userAnswers = {};
      for (let [key, value] of formData.entries()) {
          userAnswers[key] = value;
      }
      if (props.onSubmit) {
          props.onSubmit(userAnswers);
      }
      setFetchParams({
        url: props.api_url,
        method: "POST",
        body: userAnswers,
      }); // Need to handle response and errors
    }

    function close_modal () {
      history.back();
    }

    return <> 
    <div id="id01" className={style.my_modal}>
  <span onClick={close_modal} className={style.my_close} title="my_close Modal">&times;</span>
  <form className={`${style["my_modal-content"]} ${style.my_animate}`} id="form" onSubmit={() => submit_form(event, props.api_url)}>
    <div className={style.my_container}>
      <h1 id="title">{props.title}</h1>
      <hr />
      {props.children}
        <div className="alert alert-danger" id="alert" style={{display: 'none'}}>
            <strong>Erreur! </strong> <span id="alert_text"></span> <a className="alert-link" id="alert_link"></a>
          </div>
        <div className={style.hidden}>
          <span className={style.psw}><a href="#">Mot de pass oublié ?</a></span>
        
        </div>
      <div className={style.my_clearfix}>
        <button type="button" onClick={close_modal} className={style.my_cancelbtn}>Annuler</button>
        <button type="submit" id="valider" className={style.my_signupbtn}>Valider</button>
      </div>
    </div>
  </form>
</div>
    </>
}