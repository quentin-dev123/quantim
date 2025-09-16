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

  const clone2 = clone.clone()
  try {
  result = json ? await response.json() : await response.text();
  } catch (err) {
    const txt = await clone2.text()
    console.log(`An error ocurred while receiving data (${txt})`)
    console.error(err)
    console.error(txt)
    return [txt, true]
  }
  return ["success", false]
}
  useEffect(() => {
    fetchAPI().then( ([r, err]) => {
      if (err) {
        setErr({err: true, msg: r})
      } else {
        setData(r)
      }
    })
  }, [url]);

  return [data, err];
};

export default useFetch;