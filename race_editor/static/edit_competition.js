function searchStudentDB(pattern) {
    student_list = [];
    for (studentID of Object.keys(studentDB)) {
        // console.log(studentID);
        student_entry = studentDB[studentID];
        student_entry["id"] = studentID;
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
        return (
            realNameSplit.slice(0, 1) +
            " (" +
            preferredName +
            ") " +
            realNameSplit.slice(1).join(" ")
        );
    }
    return realName;
}

function filterOutExisting(search_results) {
    // let JSONResults = toJSON();
    // let filtered = [];
    // for (result of search_results) {
    //     if (!JSONResults.some((e) => e.student_id === result["item"]["id"])) {
    //         filtered.push(result);
    //     }
    // }
    // return filtered;
    return search_results;
}

function updateSearchHTML() {
    let search = document.getElementById("search_box").value;
    search_table_body.replaceChildren();
    let search_results = filterOutExisting(searchStudentDB(search));
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
        button.textContent = formatName(
            result.item.name,
            result.item.preferred_name
        );
        button.dataset.studentID = result["item"]["id"];
        button.addEventListener("click", function () {
            addStudentToResults(this.dataset.studentID);
        });
        cell.appendChild(button);
        row.appendChild(cell);
        document.getElementById("search_table_body").appendChild(row);
    }
}

function addResultElement(studentID, resultID, score=null) {
    let row = document.createElement("tr");

    let name = document.createElement("td");
    name.textContent = formatName(
        studentDB[studentID].name,
        studentDB[studentID].preferred_name
    );
    row.appendChild(name);

    let score_cell = document.createElement("td");

    let score_input = document.createElement("input");
    score_input.value = score;
    score_input.classList.add("score_input");
    score_input.dataset.studentID = studentID;
    score_input.dataset.resultID = resultID;
    score_cell.appendChild(score_input);

    row.appendChild(score_cell);

    let remove_cell = document.createElement("td");
    let remove_button = document.createElement("button");
    remove_button.addEventListener("click", deleteButton);
    remove_button.textContent = "-";
    remove_cell.appendChild(remove_button);

    row.appendChild(remove_cell);

    document.getElementById("table_body").appendChild(row);

    search_box.value = "";
    search_table_body.replaceChildren();
    document.getElementById("search_box").focus();
}

async function addStudentToResults(studentID) {
    resultID = await serverAddResult(studentID);
    addResultElement(studentID, resultID);
}

async function deleteButton() {
    let result_id =
        this.parentElement.parentElement.getElementsByClassName(
            "score_input"
        )[0].dataset.resultID;
    let delete_request_status = await serverDeleteResult(result_id);
    if (delete_request_status === 200) {
        this.parentElement.parentElement.remove();
    } else {
        alert(
            "Error in deletion. Inform support of the error code " +
                delete_request_status
        );
    }
}

function toJSON() {
    let inputs = document.getElementsByClassName("score_input");
    let scores = [];
    for (let i = 0; i < inputs.length; i++) {
        let result_content = {
            id: inputs[i].dataset.resultID,
            student_id: inputs[i].dataset.studentID,
            score: inputs[i].value,
        };
        scores.push(result_content);
    }
    return scores;
}

async function serverAddResult(studentID) {
    let response = await fetch("/add_result/" + competitionID, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            student_id: studentID,
            competition_id: competitionID,
        }),
    });
    if (response.status !== 200) {
        alert(
            "An error occurred in" +
                "serverAddResult cite code: " +
                response.status
        );
        throw Error("serverAddResult status " + response.status);
    }
    let body = await response.text();
    console.log(body);
    return body;
}

async function serverDeleteResult(resultID) {
    let response = await fetch("/delete_result/" + resultID, {
        method: "DELETE",
    });
    return response.status;
}

async function save() {
    let response = await fetch("/save_competition/" + competitionID, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toJSON()),
    });
    let body = await response.text();
    console.log(body);
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
