function myFunction() {
    var y = document.getElementById("regiao").value;
    var option = document.createElement("option");
        
    if (y === ''){
        document.getElementById("estado").innerHTML=option.remove;
    }

    if (y === 'norte') {
        document.getElementById("estado").innerHTML="<option value=amazonas>Amazonas</option><option>Pará</option>";
    }

    if (y === 'nordeste') {
        document.getElementById("estado").innerHTML="<option>Bahia</option><option>Salvador</option>";
    }

    if (y === 'centrooeste') {
        document.getElementById("estado").innerHTML="<option>Brasília</option><option>Goías</option>";
    }

    if (y === 'sudeste') {
        document.getElementById("estado").innerHTML="<option>São Paulo</option><option>Rio de Janeiro</option>";
    }

    if (y === 'sul') {
        document.getElementById("estado").innerHTML="<option>Santa Catarina</option><option>Paraná</option>";
    }
}

function estado() {
    g = document.getElementById("regiao").value;
    s = document.getElementById("estado").value;
    window.alert (s)
}