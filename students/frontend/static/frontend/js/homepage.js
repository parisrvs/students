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

    disable();
    prevent_default = true;

    request.onload = () => {
        const res = JSON.parse(request.responseText);
        enable();
        prevent_default = false;
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