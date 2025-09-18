async function Fetch ({url, json=true, method="GET", body=null}){
  try{
    const apiBaseUrl = import.meta.env.VITE_BACKEND_URL;
    const apiUrl = url.startsWith('/api') ? apiBaseUrl+url: url;
    console.log(apiUrl)
    var response = await fetch(apiUrl, {
      method: method,
      body: body ? JSON.stringify(body) : null,
      headers: body ? {
            'Content-Type': 'application/json'
        } : {}, 
    })
    var clone = response.clone()
    if (response.ok) {
      try {
        var result = json ? await response.json() : await response.text();
        console.log("Success while fetching")
        return [result, false]
      } catch(err) {
        console.error(err)
        return [err, true]
      }
    } 

    if (clone) {
      try {
        const clone2 = clone.clone()
        var txt = await clone2.text()
      } catch(err) {
        console.error(err)
        return ["Une erreur s'est produite en recevant les données du serveur (l. 38)", true]
      }
      try {
        var jsonR = await clone.json()
        return [jsonR, true];
      } catch (err) {
        console.error(err)
        return [txt, true]
      }
      
    } 

    return ["No valid response received from server", true]


  } catch (err) {
    console.error(err)
    return ["An error ocurred while fetching", true]
  }
}

export default Fetch;