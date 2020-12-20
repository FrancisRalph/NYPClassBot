# NYPClassBot
<img src="https://i.imgur.com/7P7b9Yn.png" width="256">
<br>
A Discord bot made with Python that converts a picture of a timetable into data using upscaling and Optical Character Recognition (OCR) AI technology and stores it in the cloud to remind the discord server whenever a lesson starts.

---
<img src="https://i.imgur.com/lcr9ZkZ.png" width="500">

---
This project is a submission for the Mini Project activity hosted by [NYP Developer Student Club](https://dsc-nyp.web.app/) lasting 7 weeks from 26th October 2020 to 18th December 2020. 

Group members: Derrick Png, Ethan Ng, Francis Ralph

## Features
#### !timetable add [name]
Registers a timetable for the server, maximum of 3.
<br>The bot will prompt the user to upload an image of a timetable from NYP's website.

<img src="https://i.imgur.com/Uwh9udE.png" width="650">
<br>
<img src="https://i.imgur.com/D4QuIYC.png" width="300">
<br>
<img src="https://i.imgur.com/rpxEDq8.png" width="500">

---
#### !timetable remove [name]
Removes the specified timetable from the server.

<img src="https://i.imgur.com/GzDtVdY.png" width="256">

---
#### !timetable list
Shows all the timetables associated with the server.

<img src="https://i.imgur.com/ZwkkI7f.png" width="300">

---
#### !timetable view [name]
Shows all entries of the specified timetable.

<img src="https://i.gyazo.com/4855b9640dd1c1c76cb02ecfe3d9429b.gif" width="500">

---
#### !timetable link [name] [day] [entry number/name]
Allows you to add links (e.g. zoom) to entries in a timetable.
<br>Entry input can be an entry's number as seen from !timetable view or a search term that matches a subject name.

<img src="https://i.imgur.com/QwOpNvV.png" width="500">
<br>
<img src="https://i.imgur.com/PBkaPgy.png" width="500">

---
## Contributions
Francis Ralph:
- User interaction with exception handling
- Regex magic
    - To process user input appropriately due to how the database is structured
- Addition of links to reminders
    - Database modification
    - Algorithm to process consecutive lessons as a merged entry 
- Heroku bot hosting set up
- Implementation of `!timetable add`, `link`
- Other cool stuff

<br>

Ethan Ng:
- Upscaler AI for upscaling before image-to-text conversion
- Raw text data cleaning and processing
    - Clean invalid data
    - Process timetable entry data into day, subject and time
- Database management
    - Construction of data structure
    - Creation of database module for ease of use
- Implementation of `!timetable list`, `remove`, `view`
- Other cool stuff

<br>

Derrick Png:
- OCR AI for image-to-text conversion
- Implementation of reminders
    - Algorithm to remind server whenever a lesson starts
- Other cool stuff

<br>

\* *Contributions are not limited to the above list, we worked together as a team! :D*