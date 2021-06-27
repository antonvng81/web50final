//
// EXPERIENCE
//
//
document.addEventListener('DOMContentLoaded', function() {

    update_experience();

    document.getElementById("ex-form").onsubmit = function (event) 
    {
        event.preventDefault();

        const title = document.getElementById("ex-title").value.replace(/(<([^>]+)>)/ig, '');
        const description = document.getElementById("ex-description").value.replace(/(<([^>]+)>)/ig, '');
        const start = document.getElementById("ex-start").value;
        const end = document.getElementById("ex-end").value;

        fetch('/applicant_create_experience_api', {
            method: 'POST',
            body: JSON.stringify({
                title: title,
                description: description,
                start: start,
                end: end
            })
        })
        .then(response => response.json())
        .then(result => { 
            
            document.getElementById("ex-title").value = "";
            document.getElementById("ex-description").value = "";
            document.getElementById("ex-start").value = "";
            document.getElementById("ex-end").value = "";  

            if( result.error !== undefined) {
                console.log(result);
            }
            else {
                update_experience();
            }
        });
    };

});

function update_experience()
{
    fetch('/applicant_get_experiences_api', {
        method: 'post'
        })
    .then(response => response.json())
    .then(result => {
        if(result.experiences !== undefined) {
            const desc = document.getElementById("ex-list");
            desc.innerHTML="";
            for(let i=0;i<result.experiences.length;i++) {
                if(i > 0){
                    desc.innerHTML += '<hr>';
                }
                make_experience(result.experiences[i]);
            }
            for(let i=0;i<result.experiences.length;i++) {
            
                make_experience_events(result.experiences[i]);
            }
        }
    })
}

function make_experience(experience) {
    document.getElementById("ex-list").innerHTML += 
    `<dl class='row'>`+   
    `<dt class='col-sm-3'>Title</dt>`+
    `<dd class='col-sm-9'>${experience.title}</dd>`+
    `<dt class='col-sm-3'>Description</dt>`+
    `<dd class='col-sm-9'>${experience.description}</dd>`+    
    `<dt class='col-sm-3'>Start Date</dt>`+
    `<dd class='col-sm-9'>${experience.start}</dd>`+        
    `<dt class='col-sm-3'>End Date</dt>`+
    `<dd class='col-sm-9'>${experience.end}</dd>`+  
    `</dl>`+
    `<button class='btn btn-primary' type='button' id='ex-remove-${experience.id}'><i class='bi-trash'></i> Remove</button>`+
    `<span> </span><button class='btn btn-primary' type='button' id='ex-copy-${experience.id}' > <i class='bi-clipboard'></i> Copy</button>`;
}

function make_experience_events(experience)
{
    document.getElementById(`ex-remove-${experience.id}`).onclick = function ()
    {
        fetch('/applicant_remove_experience_api', {
            method: 'POST',
            body: JSON.stringify({
                id: experience.id
            })
        })
        .then(response => response.json())
        .then(result => { 
            
            if( result.error !== undefined) {
                console.log(result);
            }
            else {
                update_experience();
            }
        });
    };

    document.getElementById(`ex-copy-${experience.id}`).onclick = function ()
    {
        document.getElementById("ex-title").value = experience.title;
        document.getElementById("ex-description").value = experience.description;
        document.getElementById("ex-start").value = experience.start;
        document.getElementById("ex-end").value = experience.end;
    };
}

