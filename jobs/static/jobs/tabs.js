


function select_tab(tab_list, selected)
{
    let i_prev = -1, i_next = -1;
    for(let i = 0; i < tab_list.length; i++)
    {
        if(document.getElementById(tab_list[i][1]).style.display === 'block')
        {
            i_prev=i;
            break;
        }
    }
    for(let i = 0; i < tab_list.length; i++)
    {
        if(tab_list[i][0] === selected)
        {
            i_next=i;
            break;
        }
    }

    if(i_next===i_prev)
        return;

    if(i_prev !== -1)
    {
        document.getElementById(tab_list[i_prev][1]).classList.remove('jobs-fade-in')
        document.getElementById(tab_list[i_prev][1]).classList.add('jobs-fade-out')

        document.getElementById(tab_list[i_prev][0]).classList.remove('jobs-fade-in')
        document.getElementById(tab_list[i_prev][0]).classList.add('jobs-fade-out')        

        setTimeout(function(){
            document.getElementById(tab_list[i_prev][0]).className = 'nav-link';
            document.getElementById(tab_list[i_prev][1]).style.display = 'none';            
        },1000*0.1);
    }   
    
    setTimeout(function(){
        document.getElementById(tab_list[i_next][0]).className = 'nav-link active';            
        document.getElementById(tab_list[i_next][1]).style.display = 'block';
        
        document.getElementById(tab_list[i_next][0]).classList.remove('jobs-fade-out')
        document.getElementById(tab_list[i_next][0]).classList.add('jobs-fade-in');

        document.getElementById(tab_list[i_next][1]).classList.remove('jobs-fade-out')
        document.getElementById(tab_list[i_next][1]).classList.add('jobs-fade-in');
    },1000*0.1);

}



function init_tabs(tab_list)
{
    for(let i = 0; i < tab_list.length; i++)
    {
        document.getElementById(tab_list[i][0]).addEventListener('click', (event) => {
            event.preventDefault();
    
            select_tab(tab_list,tab_list[i][0]);
        });

        document.getElementById(tab_list[i][0]).className = 'nav-link';
        document.getElementById(tab_list[i][1]).style.display = 'none';
    }

    select_tab(tab_list,tab_list[0][0]);
}

function create_table(){
    tab_list = [];
    query = document.querySelectorAll(".jobs-nav > .nav-item > .nav-link");

    for(let i = 0; i < query.length; i++){
        tab_list.push([
            query[i].id,
            query[i].getAttribute("data-panel")
        ]);
    }
    console.log(tab_list)

    init_tabs(tab_list);
}

document.addEventListener('DOMContentLoaded', function() {

    create_table();

});
