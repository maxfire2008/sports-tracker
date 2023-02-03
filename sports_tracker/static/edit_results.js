let counter = 0;

function uniqueID() {
    counter += Math.round(Math.random() * 25);
    generated = counter;
    counter += 25;
    return generated;
}

let progressItems = [];

function updateProgressNotice() {
    if (progressItems.length > 0) {
        document.body.classList.add('progress-cursor');
        // console.log("Progress: " + progressItems.length + " items");
    } else {
        document.body.classList.remove('progress-cursor');
        // console.log("No progress happening");
    }
}

function addWaitItem() {
    let progressID = uniqueID();
    progressItems.push(progressID);
    updateProgressNotice();
    return progressID;
}

function removeWaitItem(waitID) {
    progressItems = progressItems.filter((e) => e !== waitID);
    updateProgressNotice();
}

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

        if (result.archived == true) {
            cell.classList.add("archived");
            cell.title += "This student is archived";
            button.classList.add("archived");
            button.title += "This student is archived";
        }

        cell.appendChild(button);
        row.appendChild(cell);
        document.getElementById("search_table_body").appendChild(row);
    }
}

function addResultElement(
    studentID,
    resultID = null,
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
        placeElem.textContent = place + 1;
    } else {
        placeElem.textContent = "NC";
        placeElem.title = "Not Calculated";

        let placeElemQuestionMark = document.createElement("sup");
        placeElemQuestionMark.textContent = "[?]";
        placeElemQuestionMark.style.color = "blue";

        placeElem.appendChild(placeElemQuestionMark);
    }
    placeElem.classList.add("place-cell");
    row.appendChild(placeElem);

    let pointsElem = document.createElement("td");
    if (points !== null) {
        pointsElem.textContent = points;
    } else {
        pointsElem.textContent = "NC";
        pointsElem.title = "Not Calculated";

        let pointsElemQuestionMark = document.createElement("sup");
        pointsElemQuestionMark.textContent = "[?]";
        pointsElemQuestionMark.style.color = "blue";

        pointsElem.appendChild(pointsElemQuestionMark);
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
            remove_button.classList.add("disabled");
            remove_button.title = "Press save to allow full deletion";
        }
        remove_button.classList.add("remove-button");
    } else {
        remove_button.textContent = "🗃️";
        if (resultID !== null) {
            remove_button.addEventListener("click", archiveButton);
        } else {
            remove_button.disabled = true;
            remove_button.classList.add("disabled");
            remove_button.title = "Press save before archiving";
        }
        remove_button.classList.add("archive-button");
    }
    remove_cell.appendChild(remove_button);

    row.appendChild(remove_cell);

    if (return_row) {
        return row;
    } else {
        document.getElementById("table_body").appendChild(row);
        document.getElementById("searchBox").value = "";
        document.getElementById("search_table_body").replaceChildren();
        document.getElementById("searchBox").focus();
    }
}

async function addStudentToResults(studentID) {
    // resultID = await apiAddResult(studentID);
    addResultElement(studentID);
}

function replaceElement(a, b) {
    console.log(a, b);
    if (a.previousElementSibling) {
        a.previousElementSibling.insertAdjacentElement("afterend", b);
    } else {
        try {
            a.parentElement.insertAdjacentElement("afterbegin", b);
        } catch (e) {
            if (!e instanceof TypeError) {
                throw e;
            }
            console.log(e);
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
    console.log(result_id);
    if (result_id === "null" || result_id === null) {
        alert(
            "Can't archive, doesn't yet exist in database. Please press the save button first."
        );
        return null;
    }
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
    if (result_id === null) {
        alert("Can't restore, doesn't yet exist in database.");
        return null;
    }
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
        if (result_id === null) {
            alert("Can't delete, doesn't yet exist in database.");
            return null;
        }
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

async function archiveButtonForHousePoints() {
    let house_point_input =
        this.parentElement.parentElement.getElementsByClassName(
            "house_point_input"
        )[0];
    let housePointID = house_point_input.dataset.housePointID;
    let housePointName = house_point_input.dataset.housePointName;
    let housePointHouseID = house_point_input.dataset.housePointHouseID;

    let archival_request_status = await apiArchiveHousePoints(housePointID);
    if (archival_request_status === 200) {
        row = await addHousePointElement(
            housePointID,
            housePointName,
            housePointHouseID,
            house_point_input.value,
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

async function restoreButtonForHousePoints() {
    let house_point_input =
        this.parentElement.parentElement.getElementsByClassName(
            "house_point_input"
        )[0];
    let housePointID = house_point_input.dataset.housePointID;
    let housePointName = house_point_input.dataset.housePointName;
    let housePointHouseID = house_point_input.dataset.housePointHouseID;

    let restore_request_status = await apiRestoreHousePoints(housePointID);
    if (restore_request_status === 200) {
        row = await addHousePointElement(
            housePointID,
            housePointName,
            housePointHouseID,
            house_point_input.value,
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

async function deleteButtonForHousePoints() {
    if (confirm("Are you sure you want to delete?")) {
        let house_point_input =
            this.parentElement.parentElement.getElementsByClassName(
                "house_point_input"
            )[0];
        let housePointID = house_point_input.dataset.housePointID;
        let delete_request_status = await apiDeleteHousePoints(housePointID);
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

async function addHousePointElement(
    id,
    name,
    house,
    points,
    archived = false,
    allow_delete = true,
    return_row = false
) {
    let row = document.createElement("tr");

    let nameCell = document.createElement("td");
    nameCell.textContent = name;
    row.appendChild(nameCell);

    let houseCell = document.createElement("td");
    houseCell.textContent = house;
    row.appendChild(houseCell);

    let pointsCell = document.createElement("td");
    let pointsInput = document.createElement("input");
    pointsInput.dataset.housePointID = id;
    pointsInput.dataset.housePointName = name;
    pointsInput.dataset.housePointHouseID = house;
    pointsInput.value = points;
    pointsInput.type = "number";
    pointsInput.classList.add("house_point_input");
    pointsCell.appendChild(pointsInput);

    let remove_cell = document.createElement("td");

    if (archived === true) {
        let restore_button = document.createElement("button");
        restore_button.textContent = "♻️";
        restore_button.addEventListener("click", restoreButtonForHousePoints);

        restore_button.classList.add("restore-button");
        remove_cell.appendChild(restore_button);
        row.classList.add("archived");
    }

    remove_cell.classList.add("remove-cell");
    let remove_button = document.createElement("button");
    if (archived === true) {
        remove_button.textContent = "🗑️";
        if (allow_delete === true) {
            remove_button.addEventListener("click", deleteButtonForHousePoints);
        } else {
            remove_button.disabled = true;
            remove_button.classList.add("disabled");
            remove_button.title = "Press save to allow full deletion";
        }
        remove_button.classList.add("remove-button");
    } else {
        remove_button.textContent = "🗃️";
        remove_button.addEventListener("click", archiveButtonForHousePoints);
        remove_button.classList.add("archive-button");
    }
    remove_cell.appendChild(remove_button);

    row.appendChild(remove_cell);

    row.appendChild(pointsCell);

    if (return_row) {
        return row;
    } else {
        document.getElementById("house_points_table_body").appendChild(row);
    }
}

function freezePage() {
    $("#saveButton").prop("disabled", true);
    // add link to edit in new tab next to save
    $("#saveButton").after(
        '<a href="' +
            window.location.href +
            '" target="_blank" class="btn btn-primary">Open new tab</a>'
    );
    $("body").css("background-color", "#54bef0");
    $("#titleLabel")
        .parent()
        .before(
            '<div class="alert alert-danger" role="alert">This item has conflicts in the database.' +
                "This page has been frozen as reference. You can choose the button at the bottom of the page" +
                " to open a new tab to continue editing.</div>"
        );
    $("textarea").prop("disabled", true);
    $("input").prop("disabled", true);
    $("select").prop("disabled", true);
    $("button").prop("disabled", true);
    setTimeout(function () {
        alert(
            "This item has conflicts in the database." +
                "This page has been frozen as reference. You can choose the button at the bottom of the page" +
                " to open a new tab to continue editing."
        );
    }, 100);
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

    let house_points_inputs =
        document.getElementsByClassName("house_point_input");
    let house_points = [];
    for (let i = 0; i < house_points_inputs.length; i++) {
        let house_point_content = {
            id: house_points_inputs[i].dataset.housePointID,
            points: house_points_inputs[i].value,
        };
        house_points.push(house_point_content);
    }

    return {
        students: scores,
        house_points: house_points,
    };
}

async function apiArchiveResult(resultID) {
    let waitID = addWaitItem();
    let response = await fetch("/api/archive_result/" + resultID, {
        method: "PATCH",
    });
    removeWaitItem(waitID);
    return response.status;
}

async function apiRestoreResult(resultID) {
    let waitID = addWaitItem();
    let response = await fetch("/api/restore_result/" + resultID, {
        method: "PATCH",
    });
    removeWaitItem(waitID);
    return response.status;
}

async function apiDeleteResult(resultID) {
    let waitID = addWaitItem();
    let response = await fetch("/api/delete_result/" + resultID, {
        method: "DELETE",
    });
    removeWaitItem(waitID);
    return response.status;
}

async function apiArchiveHousePoints(resultID) {
    let waitID = addWaitItem();
    let response = await fetch("/api/archive_house_points/" + resultID, {
        method: "PATCH",
    });
    removeWaitItem(waitID);
    return response.status;
}

async function apiRestoreHousePoints(resultID) {
    let waitID = addWaitItem();
    let response = await fetch("/api/restore_house_points/" + resultID, {
        method: "PATCH",
    });
    removeWaitItem(waitID);
    return response.status;
}

async function apiDeleteHousePoints(resultID) {
    let waitID = addWaitItem();
    let response = await fetch("/api/delete_house_points/" + resultID, {
        method: "DELETE",
    });
    removeWaitItem(waitID);
    return response.status;
}

async function apiAddParticipationPoints() {
    let waitID = addWaitItem();
    let response = await fetch(
        "/api/add_participation_points/" + competitionID,
        {
            method: "POST",
        }
    );
    removeWaitItem(waitID);
    return response.status;
}

async function apiSaveCompetition() {
    let waitID = addWaitItem();
    let response = await fetch("/api/save_results/" + competitionID, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toJSON()),
    });
    let body = await response.text();
    console.log(body);
    removeWaitItem(waitID);
    if (response.status === 200) {
        window.location.reload();
    } else if (response.status === 409) {
        freezePage();
    } else {
        alert("Save failed" + response.status + response.statusText);
    }
}

async function addParticipationPointsButtonAction() {
    let response = await apiAddParticipationPoints();
    if (response === 200) {
        apiSaveCompetition();
    } else {
        alert("Error adding participation points");
    }
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

document
    .getElementById("addParticipationPointsButton")
    .addEventListener("click", addParticipationPointsButtonAction);

addEventListener("beforeunload", (event) => {});
onbeforeunload = (event) => {};
