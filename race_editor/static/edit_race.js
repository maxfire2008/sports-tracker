let id = 0;

function getUniqueId() {
    return id++ + '';
}

let student_map = {};

function new_row() {
    let row_id = getUniqueId();
    let row = document.createElement("tr");
    row.classList.add("student");
    let student_name_container = document.createElement("td");
    let student_name_select = document.createElement("select");
    student_name_select.id = "student_name_select"+row_id;
    let blank_option = document.createElement("option");
    blank_option.textContent = "-";
    student_name_select.appendChild(blank_option);
    for (let student_id of Object.keys(student_db)) {
        let student_entry = student_db[student_id];
        console.log(student_id, student_entry);
        let student_option = document.createElement("option");
        let smap_id = getUniqueId();
        student_map[smap_id] = student_id;
        student_option.value = smap_id;
        student_option.textContent = student_entry["name"];
        student_name_select.appendChild(student_option);
    }
    student_name_container.appendChild(student_name_select);
    student_name_container.innerHTML += "<div id=\"fuzzSearch"+row_id+"\">\n" +
        "  <div>\n" +
        "    <span class=\"fuzzName\"></span>\n" +
        "    <span class=\"fuzzArrow\"></span>\n" +
        "  </div>\n" +
        "  <div>\n" +
        "    <input type=\"text\" value=\"\" class=\"fuzzMagicBox\" placeholder=\"search..\" />\n" +
        "    <span class=\"fuzzSearchIcon\"></span>\n" +
        "    <ul>\n" +
        "    </ul>\n" +
        "  </div>\n" +
        "</div>";

    row.appendChild(student_name_container);
    let time_container = document.createElement("td");
    let time_input = document.createElement("input");
    time_container.appendChild(time_input);
    row.appendChild(time_container);
    document.getElementById("table_body").appendChild(row);

    $("#student_name_select"+row_id).fuzzyDropdown({
        mainContainer: '#fuzzSearch'+row_id,
        arrowUpClass: 'fuzzArrowUp',
        selectedClass: 'selected',
        enableBrowserDefaultScroll: true
    });
}

function toJSON() {
    $(".student").each(function (student) {
        console.log(student);
    })
}