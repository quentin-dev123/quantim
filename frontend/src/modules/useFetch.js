import { useState, useEffect } from "react";

const useFetch = (url, json=True, method="GET", body=null) => {
  const [data, setData] = useState(null);
    const [err, setErr] = useState({err: false, msg: ""});

  useEffect(() => {
    fetch(url, {
        method: method,
        headers: body ? {
            'Content-Type': 'application/json'
        } : {},
        body: body ? JSON.stringify(body) : null
    })
      .then((res) => json ? res.json() : res.text())
      .then((data) => setData(data))
      .catch((err) => {
        console.error("Error fetching data:", err);
        setErr({err: true, msg: err.message});
      }
    );

  }, [url]);

  return [data, err];
};

export default useFetch;