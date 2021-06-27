# Jobs
This project is about a web page for search jobs online for the applicants and create new job offerts y the employers, similarly to other web pages like infojobs.

## Functional description

*Applicant:*

- CV:
The applicants can write here their curriculums and basic data in a formulary. Also can add a list of education titles and laboral experience that can be used by the employer.

- Search jobs:
From the applicant view, once registered, he can search for jobs according to key words and the location of the offer. 
The Job descripton includes some fields like title of the job, short description, company, locations and salary.
When the user clicks to one offer, it is shown a new page where user can write a letter and apply for the jobs.

- Applied jobs:
Once applied to a job, user can see a list of all applied jobs an their state. It can be 'Not Viewed',"Viewed","Continues" and "Selected".

- Home:
Here the user can view CV data in a table.

*Employer:*

- Company:
Here the employer can edit descriptive data of the company.

- Create:
Here the employer can create a new job offer. He can insert data like title, location, salay and description.

- Jobs:
Here the employer can see the jobs he has created. Each one has two buttons for edit the job or to see the current applicants for that job.

- Applicant:
This page determine the state of the selection proccess.

- Home:
Here the emplyer can see a table with company description.

## Technical

### Models
The database models are ```User, Company, CV, Job, Application, Education, Experience```. The User model has a ```role``` field to determine if it is an applicant or an employer. Each ```Company``` and ```CV``` have an ```User```.
Each ```Job``` has a ```Company``` and each ```Application, Education, Experience``` have a ```CV```.
Models can be edited by ```admin``` page.

### Views
The backend has been writed using django python code and html templates. 

It is used ```request.POST``` data to retrieve information from the frontend. 
Then, the view create information to modify models or to send information back to frontend. 

For example, in ``` applicant_job_list_view```, the view creates a query to ```Job``` model, based on applicant's search. It can search many words at a time using ```Q``` objects. Then, it generates a ```Page``` object. Finally, renders the template, which uses parameters from the view.

In each view, information is passed to ```render``` function to customize navigation bar.

Some views have saved data to ```request.session``` object. For example: ``` applicant_job_list_view``` uses session to determine wich ```Page``` object has to be shown.

Each view is registered in ```urls.py``` file. Some views have arguments and are separated '/' characters on the url.

### Apis
There are some apis functions to retrieve and send data from the models. Each have a suffix ```api``` on the view's name. These apis are called from javascrit code in frontend using ```JSON``` and the ```fetch``` command.

### Templates
There is an html template for each view. Templates use data objects passed as arguments to ```render``` function from the views. 
Each template extends ```layout.html``` page. In it is created the navigation bar.
Some pages use pagination objects. For example, ``` applicant_job_list_view```. In it can be shown ten pagesat time and there are navigation buttons to go to next pages. All are inverse ordered by date.

### Javascript
In the ```applicant_edit_cv``` page, it is used javascript code to send and retrieve information from the models about education and experience of the applicant. In order to achieve that, some api functions have been created with the ```api``` suffix in its name, and from the frontend, it is used the ```fetch``` function to dinamically process the data of the server. The data is processed using ```JSON``` format.

Some pages have a secondary navigation bar with tabs. These tabs determine which part of the one-page html is shown. This is made by the ```tabs.js``` code that searchs ```nav-links``` and generate events to show the panels. 

### CSS
The look of the page has been created with css, and library bootstrap styles. Each page has a ```jumbotron``` with a title and a description.
