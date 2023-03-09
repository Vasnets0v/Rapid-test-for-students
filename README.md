# Rapid test for students
## Overview
The purpose of this project is to provide a tool for mentors to assess the knowledge of their students. The tool allows students to take tests without the need for registration, making it easier and more accessible for them to participate. All students need to do is indicate their group, first name, and last name to begin the testing process.

By utilizing this project, mentors can easily create and administer tests to their students, allowing them to evaluate their understanding of the material covered in class. This project aims to simplify the testing process for both mentors and students alike, making it a valuable tool in the educational setting.

## Quick start
### For Windows
First of all, open the console and follow this instruction:
1. Clone repository `git clone https://github.com/Vasnets0v/Rapid-test-for-students.git`
2. Open the folder `cd Rapid-test-for-students`
3. Create new environment `python -m venv venv`
4. Activate the environment `.\venv\Scripts\activate`
5. Install packages `pip install -r requirements.txt`
6. Start in consol `python install_project.py [email] [name] [surname] [password]` to create directories and main database with the first admin. <br> *Other administrators can be added from the admin panel.*
7. Open the folder `cd application`
8. Type `python __init__.py` in the console to start the website<br/>

Сongratulation! You can use the website.
## Web application screenshots
**The screenshots show the main features**
### Main page
The screenshot below shows the main page.
![Screenshot 1](/doc/Screenshots/scr1.png)

### Student result
The screenshot below shows the page that contains the users results. We can reset result or download sheet (.xlsx).
![Screenshot 2](/doc/Screenshots/scr2.png)

### Admin panel
This screenshot shows the admin panel where we can add new admins, create new tests, change properties or edit tests.
![Screenshot 3](/doc/Screenshots/scr3.png)

### Testing
The screenshot below shows a test page from a PC.
![Screenshot 4](/doc/Screenshots/scr4.png)

### View from mobile device
The screenshot below shows a test page from a mobile device.
![Screenshot 5](/doc/Screenshots/scr5.png)