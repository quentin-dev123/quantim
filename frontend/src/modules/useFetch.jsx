import { useState, useEffect } from "react";

const useFetch = ({url, json=true, method="GET", body=null}) => {
  const [data, setData] = useState(null);
    const [err, setErr] = useState({err: false, msg: ""});
    const [clone, setClone] = useState(null);

const fetchAPI = async () => {
  try{
    const response = await fetch(url)
    setClone(response.clone())
  } catch (err) {
    console.error(err)
    return ["An error ocurred while fetching", true]
  }
  
  if (clone) {
    const clone2 = clone.clone()
    var txt = await clone2.text()
  }  
  try {
  result = json ? await clone.json() : await clone.text();
  } catch (err) {
    console.error(err)
    console.error(txt ? txt : "No parsable text received")
    return [txt ? txt : "An error ocurred while receiving and parsing data", true]
  }
  return ["success", false]
}
  useEffect(() => {
    if (url) {
    fetchAPI().then(([r, err]) => {
      if (err) {
        setErr({err:true, msg:r})
      } else {
        setData(r)
      }
    })
  }
  }, [url]);

  return [data, err];
};

export default useFetch;