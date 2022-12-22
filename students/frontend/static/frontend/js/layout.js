var prevent_default = false;
window.addEventListener('beforeunload', function (e) {
    if (prevent_default) {
        e.preventDefault();
        e.returnValue = 'Are you sure you want to cancel this process?';
    }
    return;
});


var page = false;

var class_choices = {
    '01': "Class I",
    '02': "Class II",
    '03': "Class III",
    '04': "Class IV",
    '05': "Class V",
    '06': "Class VI",
    '07': "Class VII",
    '08': "Class VIII",
    '09': "Class IX",
    '10': "Class X",
    '11': "Class XI",
    '12': "Class XII"
}


var gender_choices = {
    'M': "Male",
    'F': "Female",
    'O': "Other",
    'N': "Non-Binary"
}

var subject_choices = {
    "PHY": "Physics",
    "CHE": "Chemistry",
    "BIO": "Biology",
    "EG1": "English Lit.",
    "EG2": "English Lang.",
    "MAT": "Mathematics",
    "HIS": "History",
    "GEO": "Geography",
    "CMP": "Computer Science",
}


document.addEventListener("DOMContentLoaded", ()=>{
    load_students(page);
});



function load_students(current_page) {
    let address = '/api/students/'
    const request = new XMLHttpRequest();
    if (current_page)
        address = current_page;

    request.open('GET', address);


    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.count) {

            let results = patch_results(res.results);

            const students_template = Handlebars.compile(document.querySelector('#studentsHandlebars').innerHTML);
            const students = students_template({
                "students": results,
                "next": res.next,
                "previous": res.previous,
                "count": res.count
            });
            document.querySelector("#students").innerHTML = students;
        }
    };

    request.send();
    return false;
}


function patch_results(results) {
    for (let x of results) {
        for (let y in x) {
            if (y === "student_class") {
                let choice = x[y];
                x[y] = class_choices[choice];
            } else if (y === "dob") {
                x[y] = convert_date(x[y]);
            } else if (y === "gender") {
                let gender = x[y];
                x[y] = gender_choices[gender];
            } else if (y === "results") {

                for (let items of x[y])
                    for (let item in items)
                        if (item === "subject") {
                            let subject = items[item];
                            items[item] = subject_choices[subject];
                        }
            }
        }
    }
    return results;
}


function convert_date (d) {
    let date = new Date(d);
    let day = date.getDate();
    let year = date.getFullYear();
    let month = date.getMonth() + 1;

    if (day < 10)
        day = `0${day}`;

    if (month < 10)
        month = `0${month}`;

    return `${day}/${month}/${year}`;
}


function change_page(p) {
    page = p;
    load_students(page);

}


function disable() {
    document.querySelectorAll('.toDisable').forEach(b => {
        b.disabled = true;
    });
    document.querySelectorAll(".toHide").forEach(s => {
        s.hidden = false;
    });
    document.querySelectorAll(".toDisableAnchorTag").forEach(a => {
        a.style.pointerEvents="none";
        a.style.cursor="default";
    });
}


function enable() {
    document.querySelectorAll('.toDisable').forEach(b => {
        b.disabled = false;
    });
    document.querySelectorAll(".toHide").forEach(s => {
        s.hidden = true;
    });
    document.querySelectorAll(".toDisableAnchorTag").forEach(a => {
        a.style.pointerEvents="auto";
        a.style.cursor="pointer";
    });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function focus_modal(modalID, inputID) {
    const myModal = document.getElementById(modalID)
    const myInput = document.getElementById(inputID)

    myModal.addEventListener('shown.bs.modal', () => {
    myInput.focus()
    })
}