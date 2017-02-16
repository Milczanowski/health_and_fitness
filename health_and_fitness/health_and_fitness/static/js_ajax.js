function makeRequest(url, type, para, on_success) {
    if (window.XMLHttpRequest) {
        http_request = new XMLHttpRequest();
        if (http_request.overrideMimeType)
            http_request.overrideMimeType('text/xml');
    }
    else if (window.ActiveXObject) {
        try {
            http_request = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try {
                http_request = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e) {
                alert(e);
            }
        }
    }

    if (!http_request) {
        addLog('Poddaję się :( Nie mogę stworzyć instancji obiektu XMLHTTP');
        return false;
    }

    http_request.onreadystatechange = function () { addContents(http_request, on_success); };
    http_request.open(type, url, true);
    http_request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");


    var token = getCookie("csrftoken");
    var parameters = "csrfmiddlewaretoken=" + token + para;
    http_request.send(parameters);
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function addContents(http_request, on_success) {
    if (http_request.readyState == 4) {
        if (http_request.status == 200) {
            var obj = JSON.parse(http_request.responseText);
            on_success(obj);
        } else {
            alert("Coś poszło nie tak")
        }
    }
}

function add_unit() {
    var unit = document.getElementById("add_unit").value;
    makeRequest("/diet/add_unit/", "POST", "&unit=" + unit, add_unit_success);
}

function add_unit_success(obj)
{
    var unit_select = document.getElementById("unit_select");
    for (var i = 0; i < obj.length; ++i) {
        var option = document.createElement("option");
        option.value = obj[i].ID;
        option.text = obj[i].Name;
        unit_select.add(option)
    }
}

function add_ingre_type()
{
    var i_t = document.getElementById("ingre_type").value;
    var i_d = document.getElementById("ingre_type_d").value;
    makeRequest("/diet/add_ingre_type/", "POST", "&name=" + i_t + "&desc=" + i_d, add_ingre_type_success);
}


function add_ingre_type_success(obj)
{
    var add_ingre_cnt = document.getElementById("add_ingre_cnt");
    for (var i = 0; i < obj.length; ++i)
    {
        var checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.name = "i_type";
        checkbox.value = obj[i].ID;
        checkbox.id = "ing_type_ch";
        add_ingre_cnt.appendChild(checkbox);
        add_ingre_cnt.innerHTML += obj[i].Name;
    }
}

function add_ingre() {
    var i_name = document.getElementById("ingre").value;
    var i_d = document.getElementById("ingre_d").value;

    var ch_box = document.getElementsByTagName("input");
    var list = []

    for (var i = 0; i < ch_box.length; ++i)
        if (ch_box[i].type == "checkbox" && ch_box[i].name == "i_type")
            if (ch_box[i].checked)
                list.push(ch_box[i].value)

    makeRequest("/diet/add_ingre/", "POST", "&name=" + i_name + "&desc=" + i_d + "&type="+JSON.stringify(list), add_ingre_success);
}


function add_ingre_success(obj) 
{
    var ingre_select = document.getElementById("ingre_select");
    for (var i = 0; i < obj.length; ++i) {
        var option = document.createElement("option");
        option.value = obj[i].ID;
        option.text = obj[i].Name;
        ingre_select.add(option)
    }
}

function add_meal_type() {
    var i_t = document.getElementById("meal_type").value;
    var i_d = document.getElementById("meal_type_d").value;
    makeRequest("/diet/add_meal_type/", "POST", "&name=" + i_t + "&desc=" + i_d, add_meal_type_success);
}


function add_meal_type_success(obj) {
    var add_ingre_cnt = document.getElementById("add_meal_cnt");
    for (var i = 0; i < obj.length; ++i) {
        var checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.name = "i_type";
        checkbox.value = obj[i].ID;
        checkbox.id = "meal_type_ch";
        add_ingre_cnt.appendChild(checkbox);
        add_ingre_cnt.innerHTML += obj[i].Name;
    }
}


function add_ingre_to_rec()
{
    var conteinter = document.getElementById("recipe_add_ingre");
    var ingre_select = document.getElementById("ingre_select");
    var unit_select = document.getElementById("unit_select");
    var number = document.getElementById("add_recipe_number").value;

    var ingre_id = ingre_select.options[ingre_select.selectedIndex].value;
    var ingre_name = ingre_select.options[ingre_select.selectedIndex].text;

    var unit_id = unit_select.options[unit_select.selectedIndex].value;
    var unit_name = unit_select.options[unit_select.selectedIndex].text;

    delete_ingre_by_id(ingre_id);

    conteinter.innerHTML += '<div id="add_ingre_list_' + ingre_id + '">\
                <input type="text" readonly="readonly" id="add_ingre_list_' + ingre_id + '_ingre" name="' + ingre_id + '" value="' + ingre_name + '"/>\
                <input type="text" readonly="readonly" id="add_ingre_list_' + ingre_id + '_number"  name="' + number + '" value="' + number + '"/>\
                <input type="text" readonly="readonly" id="add_ingre_list_' + ingre_id + '_unit"  name="' + unit_id +  '" value="' + unit_name +  '"/>\
                <button onclick="delete_ingre_by_id(' + ingre_id + ')">DELETE</button>\
            </div>';
}

function delete_ingre_by_id(id) {
    var conteinter = document.getElementById("recipe_add_ingre");

    var el = document.getElementById("add_ingre_list_" + id);

    if (el!=null)
        conteinter.removeChild(el);
}


function add_recipe()
{
    var query = Object();

    query.r_name = document.getElementById("recipe_n").value;
    query.r_desc = document.getElementById("recipe_d").value;
    query.r_time = document.getElementById("recipe_t").value;
    query.r_diff = document.getElementById("recipe_di").value;

    var conteinter = document.getElementById("recipe_add_ingre");

    query.ingre_list = []

    for (var i = 0; i < conteinter.childElementCount; ++i) {
        var ingre = Object();
        ingre.ingre_id = document.getElementById(conteinter.children[i].id + "_ingre").name;
        ingre.number     = document.getElementById(conteinter.children[i].id + "_number").name;
        ingre.unit_id  = document.getElementById(conteinter.children[i].id + "_unit").name;
        query.ingre_list.push(ingre);
    }

    var ch_box = document.getElementsByTagName("input");
    query.types = []

    for (var i = 0; i < ch_box.length; ++i)
        if (ch_box[i].type == "checkbox" && ch_box[i].name == "recipe_type")
            if (ch_box[i].checked)
                query.types.push(ch_box[i].value)

    makeRequest("/diet/add_recipe/", "POST", "&recipe=" + JSON.stringify(query), add_recipe_success);
}

function add_recipe_success(obj)
{
    alert(obj.com);
}