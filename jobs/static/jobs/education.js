//
// EDUCATION
//
//
document.addEventListener('DOMContentLoaded', function() {

    update_education();

    document.getElementById("ed-form").onsubmit = function (event) 
    {
        event.preventDefault();

        const title = document.getElementById("ed-title").value.replace(/(<([^>]+)>)/ig, '');
        const center = document.getElementById("ed-center").value.replace(/(<([^>]+)>)/ig, '');
        const start = document.getElementById("ed-start").value;
        const end = document.getElementById("ed-end").value;

        fetch('/applicant_create_education_api', {
            method: 'POST',
            body: JSON.stringify({
                title: title,
                center: center,
                start: start,
                end: end
            })
        })
        .then(response => response.json())
        .then(result => { 
            
            document.getElementById("ed-title").value = "";
            document.getElementById("ed-center").value = "";
            document.getElementById("ed-start").value = 0;
            document.getElementById("ed-end").value = "";  

            if( result.error !== undefined) {
                console.log(result);
            }
            else {
                update_education();
            }
        });
    };

});

function update_education()
{
    fetch('/applicant_get_educations_api', {
        method: 'post'
        })
    .then(response => response.json())
    .then(result => {
        if(result.educations !== undefined) {
            const desc = document.getElementById("ed-list");
            desc.innerHTML="";
            for(let i=0;i<result.educations.length;i++) {
                if(i > 0){
                    desc.innerHTML += '<hr>';
                }
                make_education(result.educations[i]);
            }
            for(let i=0;i<result.educations.length;i++) {
            
                make_education_events(result.educations[i]);
            }
        }
    })
}

function make_education(education) {
    document.getElementById("ed-list").innerHTML += 
    `<dl class='row'>`+   
    `<dt class='col-sm-3'>Title</dt>`+
    `<dd class='col-sm-9'>${education.title}</dd>`+
    `<dt class='col-sm-3'>Center</dt>`+
    `<dd class='col-sm-9'>${education.center}</dd>`+    
    `<dt class='col-sm-3'>Start Date</dt>`+
    `<dd class='col-sm-9'>${education.start}</dd>`+        
    `<dt class='col-sm-3'>End Date</dt>`+
    `<dd class='col-sm-9'>${education.end}</dd>`+  
    `</dl>`+
    `<button class='btn btn-primary' type='button' id='ed-remove-${education.id}'><i class='bi-trash'></i> Remove</button>`+
    `<span> </span><button class='btn btn-primary' type='button' id='ed-copy-${education.id}' > <i class='bi-clipboard'></i> Copy</button>`;
}

function make_education_events(education)
{
    document.getElementById(`ed-remove-${education.id}`).onclick = function ()
    {
        fetch('/applicant_remove_education_api', {
            method: 'POST',
            body: JSON.stringify({
                id: education.id
            })
        })
        .then(response => response.json())
        .then(result => { 
            
            if( result.error !== undefined) {
                console.log(result);
            }
            else {
                update_education();
            }
        });
    };

    document.getElementById(`ed-copy-${education.id}`).onclick = function ()
    {
        document.getElementById("ed-title").value = education.title;
        document.getElementById("ed-center").value = education.center;
        document.getElementById("ed-start").value = education.start;
        document.getElementById("ed-end").value = education.end;
    };
}

