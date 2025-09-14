import style from "../style/form.module.css"
import { useFetch } from "../modules/modules.js";
import { icons, bootstrap, tooltip } from "../modules/stylesheets.js";

export default function Form(props){
    useImportCSS("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css");
    useImportCSS("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css");
    useImportCSS("https://fonts.googleapis.com/icon?family=Material+Icons");
    useImportCSS("https://timothee123456.github.io/library/tooltip/style.css");
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
  icons();
  bootstrap();
  tooltip();

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