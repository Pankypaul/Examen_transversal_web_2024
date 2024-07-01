document.addEventListener('DOMContentLoaded', function(){
    const maximo = parseInt(document.getElementById('cantidadPage').innerText);
    const botonSumar = document.getElementById('botonSumarPage');
    const botonRestar = document.getElementById('botonRestarPage');
    const numeroInput = document.getElementById('numeroPage');
    const cantidadInput = document.getElementById('cantidadInput');

    botonSumar.addEventListener('click', function(){
        let currentValue = parseInt(numeroInput.value);
        if (currentValue < maximo) {
            numeroInput.value = currentValue + 1;
            cantidadInput.value = currentValue + 1;
        }else{
            alert('No puedes sumar más');
        }
    });

    botonRestar.addEventListener('click', function(){
    let currentValue = parseInt(numeroInput.value);
    if (currentValue > 1) {
        numeroInput.value = currentValue - 1;
        cantidadInput.value = currentValue - 1;
    }else{
        alert('No puedes restar más');
    }
    });

    numeroInput.addEventListener('input', function() {
        let currentValue = parseInt(numeroInput.value);
        if (currentValue > maximo) {
            numeroInput.value = maximo;
            cantidadInput.value = maximo;
        } else if (currentValue < 1) {
            numeroInput.value = 1;
        }
    });
});