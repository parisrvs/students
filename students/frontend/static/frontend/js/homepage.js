var add_student_class_choices = [
    {"key": '01', "value": "Class I"},
    {"key": '02', "value": "Class II"},
    {"key": '03', "value": "Class III"},
    {"key": '04', "value": "Class IV"},
    {"key": '05', "value": "Class V"},
    {"key": '06', "value": "Class VI"},
    {"key": '07', "value": "Class VII"},
    {"key": '08', "value": "Class VIII"},
    {"key": '09', "value": "Class IX"},
    {"key": '10', "value": "Class X"},
    {"key": '11', "value": "Class XI"},
    {"key": '12', "value": "Class XII"},
]


var add_student_gender_choices = [
    {"key": 'M', "value": "Male"},
    {"key": 'F', "value": "Female"},
    {"key": 'O', "value": "Other"},
    {"key": 'N', "value": "Non-Binary"},
]


var add_result_subject_choices = [
    {"key" :"PHY", "value": "Physics"},
    {"key" :"CHE", "value": "Chemistry"},
    {"key" :"BIO", "value": "Biology"},
    {"key" :"EG1", "value": "English Lit."},
    {"key" :"EG2", "value": "English Lang."},
    {"key" :"MAT", "value": "Mathematics"},
    {"key" :"HIS", "value": "History"},
    {"key" :"GEO", "value": "Geography"},
    {"key" :"CMP", "value": "Computer Science"}
]


function display_add_student_modal() {
    const add_student_modal_template = Handlebars.compile(document.querySelector('#addStudentModalHandlebars').innerHTML);
    const add_student_modal = add_student_modal_template({
        "class_choices": add_student_class_choices,
        "gender_choices": add_student_gender_choices
    });
    document.querySelector("#addStudentModal").innerHTML = add_student_modal;
    document.querySelector("#addStudentModalBtn").click();
    focus_modal("addStudentModal", "student_name");
    return false;
}


function add_student() {
    let name = document.querySelector("#student_name").value.replace(/^\s+|\s+$/g, '');
    let student_class = document.querySelector("#student_class").value.replace(/^\s+|\s+$/g, '');
    let student_gender = document.querySelector("#student_gender").value.replace(/^\s+|\s+$/g, '');
    let student_roll_number = document.querySelector("#student_roll_number").value.replace(/^\s+|\s+$/g, '');
    let student_dob = document.querySelector("#student_dob").value.replace(/^\s+|\s+$/g, '');
    let student_mobile = document.querySelector("#student_mobile").value.replace(/^\s+|\s+$/g, '');

    if (!name || !student_class || !student_gender || !student_roll_number || !student_dob || !student_mobile) {
        document.querySelector("#add_student_error").innerHTML = "Incomplete Form";
        return false;
    }

    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/api/students/');
    request.setRequestHeader("X-CSRFToken", csrftoken);

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (request.status === 400) {
            document.querySelectorAll(".errormessage").forEach(e => {
                e.innerHTML = '';
            });
            for (msg in res) {
                let id = `feedback_${msg}`
                if (document.getElementById(id))
                    document.getElementById(id).innerHTML = res[msg][0];
            }
        } else if (request.status === 201) {
            page = false;
            load_students(page);
            document.querySelector("#addStudentModalCloseBtn").click();
        }
    };

    const data = new FormData();
    data.append('name', name);
    data.append('student_class', student_class);
    data.append('gender', student_gender);
    data.append('roll_number', student_roll_number);
    data.append('dob', student_dob);
    data.append('mobile', student_mobile);
    request.send(data);
    return false;
}


function display_add_result_modal(student_id) {
    const add_result_modal_template = Handlebars.compile(document.querySelector('#addResultModalHandlebars').innerHTML);
    const add_result_modal = add_result_modal_template({
        "subject_choices": add_result_subject_choices,
        "student_id": student_id
    });
    document.querySelector("#addResultModal").innerHTML = add_result_modal;
    document.querySelector("#addResultModalBtn").click();
    focus_modal("addResultModal", "subject_name");
    return false;
}



function add_result(student_id) {
    let subject_name = document.querySelector("#subject_name").value.replace(/^\s+|\s+$/g, '');
    let maximum_marks = document.querySelector("#maximum_marks").value.replace(/^\s+|\s+$/g, '');
    let marks_obtained = document.querySelector("#marks_obtained").value.replace(/^\s+|\s+$/g, '');
    let remarks = document.querySelector("#remarks").value.replace(/^\s+|\s+$/g, '');

    if (!subject_name || !maximum_marks || !marks_obtained || !remarks) {
        document.querySelector("#add_result_error").innerHTML = "Incomplete Form";
        return false;
    }

    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', `/api/students/${student_id}/results/`);
    request.setRequestHeader("X-CSRFToken", csrftoken);

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (request.status === 400) {
            document.querySelectorAll(".errormessage").forEach(e => {
                e.innerHTML = '';
            });
            for (msg in res) {
                if (msg === "non_field_errors") {
                    document.querySelector("#add_result_error").innerHTML = res[msg];
                }
                let id = `feedback_${msg}`
                if (document.getElementById(id))
                    document.getElementById(id).innerHTML = res[msg][0];
            }
        } else if (request.status === 201) {
            page = false;
            load_students(page);
            document.querySelector("#addResultModalCloseBtn").click();
        }
    };

    const data = new FormData();
    data.append('subject', subject_name);
    data.append('max_marks', maximum_marks);
    data.append('marks_obtained', marks_obtained);
    data.append('remark', remarks);
    request.send(data);
    return false;


}