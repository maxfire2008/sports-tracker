function searchStudentDB(pattern) {
    student_list = [];
    for (student_id of Object.keys(studentDB)) {
        // console.log(student_id);
        student_entry = studentDB[student_id];
        student_entry["id"] = student_id;
        student_list.push(student_entry);
    }
    const options = {
        // isCaseSensitive: false,
        // includeScore: false,
        // shouldSort: true,
        // includeMatches: false,
        // findAllMatches: false,
        // minMatchCharLength: 1,
        // location: 0,
        // threshold: 0.6,
        // distance: 100,
        // useExtendedSearch: false,
        // ignoreLocation: false,
        // ignoreFieldNorm: false,
        // fieldNormWeight: 1,
        keys: ["name", "preferred_name", "id"],
    };

    const fuse = new Fuse(student_list, options);

    return fuse.search(pattern);
}

function updateSearchHTML() {
    let search_results = searchStudentDB(
        document.getElementById("search_box").value
    );
    search_table_body.replaceChildren();
    for (result of search_results) {
        let row = document.createElement("tr");
        let cell = document.createElement("td");
        let button = document.createElement("button");
        button.textContent = result.item.name;
        button.dataset.item = JSON.stringify(result["item"]);
        button.addEventListener("click", function () {
            addStudentToResults(JSON.parse(this.dataset.item));
        });
        cell.appendChild(button);
        row.appendChild(cell);
        document.getElementById("search_table_body").appendChild(row);
    }
}

function addStudentToResults(student_data) {
    let row = document.createElement("tr");

    let name = document.createElement("td");
    name.textContent = student_data["name"];
    row.appendChild(name);

    let score_cell = document.createElement("td");

    let score_input = document.createElement("input");
    score_input.classList.add("student_time");
    score_input.dataset.student_id = student_data["id"];
    score_cell.appendChild(score_input);

    row.appendChild(score_cell);

    document.getElementById("table_body").appendChild(row);

    search_box.value = "";
    search_table_body.replaceChildren();
    document.getElementById("search_box").focus();
}

document
    .getElementById("search_box")
    .addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            let search_results = searchStudentDB(
                document.getElementById("search_box").value
            );
            addStudentToResults(search_results[0]["item"]);
        }
    });

document
    .getElementById("search_box")
    .addEventListener("input", updateSearchHTML);

window.addEventListener("load", function () {
    search_box.value = "";
});
