import { useState, useEffect } from "react";

const useFetch = ({url, json=true, method="GET", body=null}) => {
  const [data, setData] = useState(null);
    const [err, setErr] = useState({err: false, msg: ""});
    var [response, setResponse] = useState(null);

  useEffect(() => {
    if (url) {
      fetch(url, {
        method: method,
        headers: body ? {
            'Content-Type': 'application/json'
        } : {},
        body: body ? JSON.stringify(body) : null
    })
      .then((res) => {
        setResponse(res.clone())
        if (res.ok) {
          json ? res.json() : res.text();
        } else {
          throw new Error(res.text())
        }
      })
      .then((data) => setData(data))
      .catch((err) => {
        console.error("Error fetching data:", err);
        setErr({err: true, msg: err.message});
        console.log(response.statusText)
        response.text().then(res => console.log(res));
      }
    );
}
  }, [url]);

  return [data, err];
};

export default useFetch;