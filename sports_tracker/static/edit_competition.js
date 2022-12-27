function searchStudentDB(pattern) {
    student_list = [];
    for (studentID of Object.keys(studentDB.students)) {
        // console.log(studentID);
        student_entry = studentDB.students[studentID];
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
    let JSONResults = toJSON().students;
    let filtered = [];
    for (result of search_results) {
        if (!JSONResults.some((e) => e.student_id === result["item"]["id"])) {
            filtered.push(result);
        }
    }
    return filtered;
    // return search_results;
}

function updateSearchHTML() {
    let search = document.getElementById("searchBox").value;
    document.getElementById("search_table_body").replaceChildren();
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

function addResultElement(
    studentID,
    resultID,
    score = null,
    archived = false,
    allow_delete = true,
    return_row = false,
    place = null,
    points = null
) {
    let row = document.createElement("tr");

    let placeElem = document.createElement("td");
    if (place !== null && place !== -1) {
        placeElem.textContent = place+1;
    } else {
        placeElem.textContent = "Not calculated";
    }
    placeElem.classList.add("place-cell");
    row.appendChild(placeElem);

    let pointsElem = document.createElement("td");
    if (points !== null) {
        pointsElem.textContent = points;
    } else {
        pointsElem.textContent = "Not calculated";
    }
    pointsElem.classList.add("points-cell");
    row.appendChild(pointsElem);

    let name = document.createElement("td");
    name.textContent = formatName(
        studentDB.students[studentID].name,
        studentDB.students[studentID].preferred_name
    );
    name.classList.add("student-name-cell");
    row.appendChild(name);

    let score_cell = document.createElement("td");
    score_cell.classList.add("score-cell");

    let score_input = document.createElement("input");
    score_input.value = score;
    score_input.classList.add("score_input");
    score_input.dataset.studentID = studentID;
    score_input.dataset.resultID = resultID;
    score_cell.appendChild(score_input);

    row.appendChild(score_cell);

    let remove_cell = document.createElement("td");

    if (archived === true) {
        let restore_button = document.createElement("button");
        restore_button.textContent = "♻️";
        restore_button.addEventListener("click", restoreButton);

        restore_button.classList.add("restore-button");
        remove_cell.appendChild(restore_button);
        row.classList.add("archived");
    }

    remove_cell.classList.add("remove-cell");
    let remove_button = document.createElement("button");
    if (archived === true) {
        remove_button.textContent = "🗑️";
        if (allow_delete === true) {
            remove_button.addEventListener("click", deleteButton);
        } else {
            remove_button.disabled = true;
        }
        remove_button.classList.add("remove-button");
    } else {
        remove_button.textContent = "🗃️";
        remove_button.addEventListener("click", archiveButton);
        remove_button.classList.add("archive-button");
    }
    remove_cell.appendChild(remove_button);

    row.appendChild(remove_cell);

    if (return_row) {
        return row;
    } else {
        document.getElementById("table_body").appendChild(row);
    }

    document.getElementById("searchBox").value = "";
    document.getElementById("search_table_body").replaceChildren();
    document.getElementById("searchBox").focus();
}

async function addStudentToResults(studentID) {
    resultID = await apiAddResult(studentID);
    addResultElement(studentID, resultID);
}

function replaceElement(a, b) {
    if (a.previousElementSibling) {
        a.previousElementSibling.insertAdjacentElement("afterend", b);
    } else {
        try {
            a.parentElement.insertAdjacentElement("afterbegin", b);
        } catch (TypeError) {
            confirm("Whoah! Slow down.");
        }
    }
    a.remove();
}

async function archiveButton() {
    let score_input =
        this.parentElement.parentElement.getElementsByClassName(
            "score_input"
        )[0];
    let result_id = score_input.dataset.resultID;
    let student_id = score_input.dataset.studentID;
    let archival_request_status = await apiArchiveResult(result_id);
    if (archival_request_status === 200) {
        row = addResultElement(
            student_id,
            result_id,
            score_input.value,
            true,
            false,
            true
        );
        replaceElement(this.parentElement.parentElement, row);
    } else {
        alert(
            "Error in archival. Inform support of the error code " +
                archival_request_status
        );
    }
}

async function restoreButton() {
    let score_input =
        this.parentElement.parentElement.getElementsByClassName(
            "score_input"
        )[0];
    let result_id = score_input.dataset.resultID;
    let student_id = score_input.dataset.studentID;
    let restore_request_status = await apiRestoreResult(result_id);
    if (restore_request_status === 200) {
        row = addResultElement(
            student_id,
            result_id,
            score_input.value,
            false,
            true,
            true
        );
        replaceElement(this.parentElement.parentElement, row);
    } else {
        alert(
            "Error in restore. Inform support of the error code " +
                restore_request_status
        );
    }
}

async function deleteButton() {
    if (confirm("Are you sure you want to delete?")) {
        let result_id =
            this.parentElement.parentElement.getElementsByClassName(
                "score_input"
            )[0].dataset.resultID;
        let delete_request_status = await apiDeleteResult(result_id);
        if (delete_request_status === 200) {
            this.parentElement.parentElement.remove();
        } else {
            alert(
                "Error in deletion. Inform support of the error code " +
                    delete_request_status
            );
        }
    }
}

async function addBonusPointElement(id, name, house, points) {
    let row = document.createElement("tr");

    let nameCell = document.createElement("td");
    nameCell.textContent = name;
    row.appendChild(nameCell);

    let houseCell = document.createElement("td");
    houseCell.textContent = house;
    row.appendChild(houseCell);

    let pointsCell = document.createElement("td");
    let pointsInput = document.createElement("input");
    pointsInput.dataset.bonusPointID = id;
    pointsInput.value = points;
    pointsInput.type="number";
    pointsInput.classList.add("bonus_point_input");
    pointsCell.appendChild(pointsInput);

    row.appendChild(pointsCell);

    document.getElementById("bonus_points_table_body").appendChild(row);
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

    let bonus_points_inputs =
        document.getElementsByClassName("bonus_point_input");
    let bonus_points = [];
    for (let i = 0; i < bonus_points_inputs.length; i++) {
        let bonus_point_content = {
            id: bonus_points_inputs[i].dataset.bonusPointID,
            points: bonus_points_inputs[i].value,
        };
        bonus_points.push(bonus_point_content);
    }

    return {
        students: scores,
        bonus_points: bonus_points,
    };
}

async function apiAddResult(studentID) {
    let response = await fetch("/api/add_result/" + competitionID, {
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

async function apiArchiveResult(resultID) {
    let response = await fetch("/api/archive_result/" + resultID, {
        method: "PATCH",
    });
    return response.status;
}

async function apiRestoreResult(resultID) {
    let response = await fetch("/api/restore_result/" + resultID, {
        method: "PATCH",
    });
    return response.status;
}

async function apiDeleteResult(resultID) {
    let response = await fetch("/api/delete_result/" + resultID, {
        method: "DELETE",
    });
    return response.status;
}

async function apiSaveCompetition() {
    let response = await fetch("/api/save_competition/" + competitionID, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toJSON()),
    });
    let body = await response.text();
    console.log(body);
    window.location.reload();
}

document
    .getElementById("searchBox")
    .addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            let search_results = filterOutExisting(
                searchStudentDB(document.getElementById("searchBox").value)
            );
            if (search_results < 1) {
                alert("No match!");
            } else {
                addStudentToResults(search_results[0]["item"]["id"]);
            }
        }
    });

document
    .getElementById("searchBox")
    .addEventListener("input", updateSearchHTML);

document
    .getElementById("saveButton")
    .addEventListener("click", apiSaveCompetition);

window.addEventListener("load", function () {
    document.getElementById("searchBox").value = "";
});
