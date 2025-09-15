import { useEffect } from 'react';

function useImportCSS(href) {
    try{
    useEffect(() => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    if (href.startsWith('./')){
        href = href.replace('./', '/src/style/'); // Adjust path if it starts with ./
    }
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