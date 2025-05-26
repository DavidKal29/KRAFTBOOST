//Menú Hamburguesa Lógica

//Obtenemos el boton para abrir o cerrar
boton_hamburguesa=document.getElementById('boton_hamburguesa')
boton_hamburguesa.addEventListener('click', ()=>{ 
    //Obtenemos el div que es el menu hamburguesa
    let menu=document.getElementById('menu_hamburguesa'); 
    
    //Vemos si el menu está escondido o no, y dependiendo de eso, lo escondemos o lo hacemos aparecer
    menu.style.right=menu.style.right==='0px'?'-100%':'0px';

    //Obtenemos el icono del boton
    let icono_boton=document.getElementById('icono_boton') 

    //Esto hace que si la classlist es una de esas, cambia a la otra
    icono_boton.classList.toggle("fa-bars"); 
    icono_boton.classList.toggle("fa-x");       
});

let desactivado = false;

//FUncion para evitar spammeo de clicks al 
// añadir o quitar cosas en el carrito
let desactivar=(a)=>{
    //Si esta desactivado el boton, devuelve false directamente
    if (desactivado) {
        return false
    }
  
    desactivado=true
    a.style.pointerEvents='none';//Esto evitara que la gente le de 500000 clicks a los enlaces
    document.body.style.pointerEvents='none'//Tambien, hacemos que no se pueda pulsar a otro boton 

    //Si está 5 segundos sin clickar, se 
    // activa de nuevo el click y la opacidad
    setTimeout(() => {
        desactivado=false;
        a.style.backgroundColor='#C40C0C'
        a.style.pointerEvents='auto'
        document.body.style.pointerEvents='auto'
    
    },5000);

    
    return true
}


console.log('El pathname:',window.location.pathname);

//Si la ruta es cualquiera salvo /shop y /admin/products (por los filtros) y tiene parámetros
if (window.location.pathname!='/shop' && window.location.pathname!='/admin/products' && window.location.search){
    
    //Limpiamos los parámetros sin recargar la página
    let newUrl=window.location.origin+window.location.pathname
    window.history.replaceState({},document.title,newUrl)

    console.log('Cambiado con exito')

}

  
