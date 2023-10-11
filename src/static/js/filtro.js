function myFunction() {
    var y = document.getElementById("regiao").value;
    var option = document.createElement("option");
    var select = document.getElementById("estado");
    if (y === ''){
        document.getElementById("estado").innerHTML=option.remove;
    }

    if (y === 'norte') {
        var est = new Array("Amazonas", "Pará", "Amapá", "Roraima", "Tocantins", "Rondônia", "Acre");
        var estval = new Array("amazonas", "para", "amapa", "roraima", "tocantins", "rondonia", "acre");
        document.getElementById("estado").innerHTML=option.remove;
        for(var i = 0; i < est.length; i++) {
            select[select.length] = new Option(est[i], estval[i])
        }
        
        // document.getElementById("estado").innerHTML="<option value=amazonas>Amazonas</option><option value=para>Pará</option>";
    }

    if (y === 'nordeste') {
        // document.getElementById("estado").innerHTML="<option>Bahia</option><option>Salvador</option>";
        var est = new Array("Pernambuco", "Maranhão", "Bahia", "Ceará", "Piauí", "Rio Grande do Norte", "Paraíba", "Sergipe", "Alagoas");
        var estval = new Array("pernambuco", "maranhão", "bahia", "ceará", "piauí", "riograndedonorte", "paraíba", "sergipe", "alagoas");
        document.getElementById("estado").innerHTML=option.remove;
        for(var i = 0; i < est.length; i++) {
            select[select.length] = new Option(est[i], estval[i])
        }
    }

    if (y === 'centrooeste') {
        // document.getElementById("estado").innerHTML="<option>Brasília</option><option>Goías</option>";
        var est = new Array("Brasília", "Mato Grosso", "Mato Grosso do Sul", "Goiás");
        var estval = new Array("brasilia", "matogrosso", "matogrossodosul", "goias");
        document.getElementById("estado").innerHTML=option.remove;
        for(var i = 0; i < est.length; i++) {
            select[select.length] = new Option(est[i], estval[i])
        }
    }

    if (y === 'sudeste') {
        // document.getElementById("estado").innerHTML="<option>São Paulo</option><option>Rio de Janeiro</option>";
        var est = new Array("São Paulo", "Rio de Janeiro", "Espírito Santo", "Minas Gerais");
        var estval = new Array("saopaulo", "riodejaneiro", "espiritosanto", "minasgerais");
        document.getElementById("estado").innerHTML=option.remove;
        for(var i = 0; i < est.length; i++) {
            select[select.length] = new Option(est[i], estval[i])
        }
    }

    if (y === 'sul') {
        // document.getElementById("estado").innerHTML="<option>Santa Catarina</option><option>Paraná</option>";
        var est = new Array("Rio Grande do Sul", "Santa Catarina", "Paraná");
        var estval = new Array("riograndedosul", "santacatarina", "parana");
        document.getElementById("estado").innerHTML=option.remove;
        for(var i = 0; i < est.length; i++) {
            select[select.length] = new Option(est[i], estval[i])
        }
    }
}

function estado() {
    g = document.getElementById("regiao").value;
    s = document.getElementById("estado").value;
    
    if (g === "") {
        window.alert ("Insira um valor válido!")
    }
    else {
        window.alert (g, s)
    }
}

function dados() {
    h = document.getElementById("dadosofc").value;

    if (h === "") {
        window.alert ("Insira um valor válido!")
    }
    
    window.alert (h)
}