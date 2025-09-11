import { useEffect } from 'react';

function useImportCSS(href) {
    try{
    useEffect(() => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href; // external CSS file URL
    document.head.appendChild(link);

    return () => {
      document.head.removeChild(link); // cleanup when component unmounts
    };
  }, []);

    return "link tag added successfully !";
    } catch(err) {
        console.log(err)
        return "An error ocurred : " + err;
    }
  
}

export default useImportCSS;