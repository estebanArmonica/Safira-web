document.oncontextmenu = function() {
    return false;
};

// desabilitamos las teclas de acceso rapido
var controlPrecionado = 0;
var altPrecionado = 0;

function bloquearTeclas(teclaActual){
    var desactivar = false;

    // Ctrl +
    if(controlPrecionado === 17){
        if(teclaActual === 78 || 
           teclaActual === 85 || 
           teclaActual === 82 || 
           teclaActual === 116 || 
           teclaActual === 114 || 
           teclaActual === 17 || 
           teclaActual === 38 || 
           teclaActual === 73
        ){
            desactivar = true;
        }
    }

    // Alt +
    if(altPrecionado === 18){
        // desabilitamos las teclas de acceso rapido
        if(teclaActual === 37 || 
           teclaActual === 39
        ){
            desactivar = true;
        }
    }

    if(teclaActual == 17) controlPrecionado=teclaActual;
    if(teclaActual == 18) altPrecionado=teclaActual;

    return desactivar;
} 

document.onkeyup = function() {
    if(window.event && window.event.keyCode === 17){
        controlPrecionado = 0;
    }

    if(window.event && window.event.keyCode === 18){
        altPrecionado = 0;
    }
}

document.onkeydown = function() {
    /* 
        116 -> F5
        122 -> F11
        114 -> F3
        117 -> F6
    */
    if(window.event && bloquearTeclas(window.event.keyCode)){
        return false;
    }

    if(window.event && 
       window.event.keyCode === 122 || 
       window.event.keyCode === 116 || 
       window.event.keyCode === 114 || 
       window.event.keyCode === 17
    ){
        window.event.keyCode == 505;
    }

    if(window.event.keyCode == 505) {
        return false;
    }

    if (window.event && (window.event.keyCode == 8)){
        valor = document.activeElement.value;
        if(valor == undefined){return false;}
    } else {
        // Evitamos los backspace en cada uno de los campos
        if(document.activeElement.getAttribute('type') == 'select-one'){return false;}
        if(document.activeElement.getAttribute('type') == 'button'){return false;}
        if(document.activeElement.getAttribute('type') == 'radio'){return false;}
        if(document.activeElement.getAttribute('type') == 'checkbox'){return false;}
        if(document.activeElement.getAttribute('type') == 'file'){return false;}
        if(document.activeElement.getAttribute('type') == 'reset'){return false;}
        if(document.activeElement.getAttribute('type') == 'submit'){return false;}
        else{
            if(document.activeElement.value.length == 0) {
                // no se realiza backspace (largo si igual a 0)
                return false;
            } else {
                // se permite el backspace
                document.activeElement.value.keyCode = 8;
            }
        } // texto, textarea, password
    }
}