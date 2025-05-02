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



///////////////////////////////////////////////////////////////////////////////////////

//Botones de Filtrado de /shop Lógica

//Obtenemos los botones de filtrado
let botones_filtro=document.querySelectorAll('.boton_filtro')
let boton_eliminar=document.getElementById('boton_eliminar')


//Recorremos cada boton de filtrado
botones_filtro.forEach(btn => {
    //Si pulsa uno de los botones, recorre todos, les pone el mismo color
    // y al pulsado le pone el color rojo de que ha sido pulsado
    btn.addEventListener('click', ()=>{
        botones_filtro.forEach(b => {
            b.classList.remove('bg-[#C40C0C]','text-white')
            b.classList.add('bg-white','text-[#C40C0C]')
        })

        btn.classList.remove('bg-white','text-[#C40C0C]')
        btn.classList.add('bg-[#C40C0C]','text-white')
    })
})


//Si pulsa borrar recorre todos y se ponen todos blancos
boton_eliminar.addEventListener('click',()=>{
    botones_filtro.forEach(b => {
        b.classList.remove('bg-[#C40C0C]','text-white')
        b.classList.add('bg-white','text-[#C40C0C]')
    })
})




