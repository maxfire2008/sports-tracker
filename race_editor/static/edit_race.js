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

function formatName(realName, preferredName) {
    realNameSplit = realName.split(" ");
    if (preferredName) {
        return realNameSplit.slice(0, 1)+" ("+preferredName+") "+realNameSplit.slice(1).join(" ");
    }
    return realName
}

function filterOutExisting(search_results) {
    filtered = [];
    for (result of search_results) {
        if (!Object.keys(toJSON()).includes(result["item"]["id"])) {
            filtered.push(result);
        }
    }
    return filtered;
}

function updateSearchHTML() {
    let search = document.getElementById("search_box").value;
    search_table_body.replaceChildren();
    let search_results = filterOutExisting(
        searchStudentDB(search)
    );
    if (search_results < 1 && search !== "") {
        let row = document.createElement("tr");
        let cell = document.createElement("td");
        cell.textContent = "No results!";
        row.appendChild(cell);
        document.getElementById("search_table_body").appendChild(row);
    }
    for (result of search_results) {
        let row = document.createElement("tr");
        let cell = document.createElement("td");
        let button = document.createElement("button");
        button.textContent = formatName(result.item.name, result.item.preferred_name);
        button.dataset.item = result["item"]["id"];
        button.addEventListener("click", function () {
            addStudentToResults(this.dataset.student_id);
        });
        cell.appendChild(button);
        row.appendChild(cell);
        document.getElementById("search_table_body").appendChild(row);
    }
}

function addStudentToResults(studentID) {
    let row = document.createElement("tr");

    let name = document.createElement("td");
    name.textContent = formatName(studentDB[studentID].name, studentDB[studentID].preferred_name);
    row.appendChild(name);

    let score_cell = document.createElement("td");

    let score_input = document.createElement("input");
    score_input.classList.add("score_input");
    score_input.dataset.student_id = studentID;
    score_cell.appendChild(score_input);

    row.appendChild(score_cell);

    document.getElementById("table_body").appendChild(row);

    search_box.value = "";
    search_table_body.replaceChildren();
    document.getElementById("search_box").focus();
}

function toJSON() {
    let inputs = document.getElementsByClassName("score_input");
    let scores = {};
    for (let i = 0; i < inputs.length; i++) {
        scores[inputs[i].dataset.student_id] = inputs[i].value;
    }
    return scores;
}

document
    .getElementById("search_box")
    .addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            let search_results = filterOutExisting(
                searchStudentDB(document.getElementById("search_box").value)
            );
            if (search_results < 1) {
                alert("No match!");
            } else {
                addStudentToResults(search_results[0]["item"]["id"]);
            }
        }
    });

document
    .getElementById("search_box")
    .addEventListener("input", updateSearchHTML);

window.addEventListener("load", function () {
    search_box.value = "";
});
