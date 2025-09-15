function Username(){
    return<>
    <input type="text" placeholder="Username" name="username" autoComplete="username" required />
    </>
}

function Email(){
    return<>
    <input type="email" placeholder="Email" name="email" id="email" required />
    </>
}

function ReceiveEmailsCheckbox(){
    return<>
    <label htmlFor="accept_notif" style={{ cursor:"pointer"}}>
        <input type="checkbox"  name="accept_notif" id="accept_notif" style={{marginBottom:"15px", cursor:"pointer"}} defaultChecked /> J'accepte de recevoir des emails
    </label>
    </>
}

export { Username, Email, ReceiveEmailsCheckbox }