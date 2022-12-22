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



function load_students(page) {
    let address = '/api/students/'
    const request = new XMLHttpRequest();
    if (page)
        address = page;
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