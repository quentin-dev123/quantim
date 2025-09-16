async function Fetch ({url, json=true, method="GET", body=null}){
console.log(body)

  try{
    var response = await fetch(url, {
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
      const clone2 = clone.clone()
      var txt = await clone2.text()
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
      } catch (err) {
        console.error(err)
        return [txt, true]
      }
      return [jsonR, true];
    }


  } catch (err) {
    console.error(err)
    return ["An error ocurred while fetching", true]
  }
}

export default Fetch;