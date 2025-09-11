export default function Form(props){
    return <> 
    <div id="id01">
  <span onclick="close_modal()" title="my_close Modal">&times;</span>
  <form id="form">
    <div>
      <h1 id="title">{props.title}</h1>
      <hr />
      {props.children}
        <div id="alert" style="display: none;">
            <strong>Erreur! </strong> <span id="alert_text"></span> <a id="alert_link"></a>
          </div>
	<div style="display:none">
		<span ><a href="#">Mot de pass oublié ?</a></span>
        
        </div>
      <div>
        <button type="button" onclick="close_modal()">Annuler</button>
        <button type="submit" id="valider">Valider</button>
      </div>
    </div>
  </form>
</div>
    </>
}