# Yalantis-Demo-Project
## Overview
In this project I created few endpoints with next functions:
* Add course to catalogue
* Display all courses in catalogue
* Show details about course (id required)
* Search by title 
* Filter by date
* Change attributes of course:
  * Title
  * Start date of the course
  * End date of the course
  * Number of lectures
* Delete course from catalogue

Input/Output - JSON


### Libraries and Frameworks
* Flask
* SQLAlchemy
* Marshmallow


## Installation
1. [Create virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
2. Install needed packages
```
pip install -r requirments.txt
```
3. Run main.py file
```
python main.py
```

## How to use
### GET

 </courses/> => return list of courses

 </courses/{id}> => return course with specified ID

### POST

</courses/> + json body
```
{
'title'       (required)
'lectures'    (optional)
'start_date'  (optional, default - today)
'end_date'    (optional)
} => return newly created course + location header with link
```

### PUT

</courses/{id}> + json body
```
{
'title'       (optional)
'lectures'    (optional)
'start_date'  (optional)
'end_date'    (optional)
} => return updated  course
```
### DELETE

</course/{id}> => return: 204

### Search and Filter

Use '?title=<search_query>' to search

Use '?start_date=<start_date>' to filter by start date
