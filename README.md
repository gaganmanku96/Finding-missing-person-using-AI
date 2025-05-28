# Find Missing Person using AI
![Issues](https://img.shields.io/github/issues/gaganmanku96/Finding-missing-person-using-AI) ![Stars](https://img.shields.io/github/stars/gaganmanku96/Finding-missing-person-using-AI?style=social)
[![Linkedin](https://img.shields.io/badge/LinkedIn-0077B6?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gaganmanku96/)
[![Medium](https://img.shields.io/badge/Medium-12100F?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@gaganmanku96)
![CodeRabbit Reviews](https://img.shields.io/coderabbit/prs/github/gaganmanku96/Finding-missing-person-using-AI?utm_source=oss&utm_medium=github&utm_campaign=gaganmanku96%2FFinding-missing-person-using-AI&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)


Hundreds of people (especially children go missing every day) in India. There are various <b>NGO's and Govt Initiatives</b> to help with it. This project tries to implement an  existing/new way to help.

## List of contents
- ### [News Articles](#news-articles)
- ### [Objective](#what-is-the-objective-of-this-project-and-how-will-it-help)
- ### [Solution](#solution-projects-implementation)
- ### [Installation](#how-to-run)
- ### [What is left/not working?](#what-is-left)

## News Articles
#### [Article 1](https://www.thehindu.com/society/indias-missing-children-what-the-whatsapp-rumours-dont-tell-you/article24641527.ece)
![News Article 1](resources/news_1.PNG)
#### [Article 2](https://www.deccanchronicle.com/nation/current-affairs/250518/indias-children-174-go-missing-every-day-half-untraced.html)
![News Article 2](resources/news_2.PNG)


## What is the objective of this Project and how will it help?
The objective of this project is to help Police and higher authorities to track down missing people quickly. The usual process to track a person is using investigation which requires time and experience (to ask right questions). Most of the time, investigation method works pretty well but it is time consuming and can be unsuccessful if the person (missing) has been shifted/moved to different location (city/country).<br>
In such cases, the ideal approach is to go through CCTV footages and evidences. Again, this can be very time consuming and given the number of people that go missing everyday, it can be a challanage to keep up with it.<br>

## Solution (Project's Implementation)

### 2025 Major Update: Migration to MediaPipe Face Mesh
- The project has migrated from dlib-based facial landmark/encoding to **MediaPipe Face Mesh** for all facial feature extraction and matching.
- All code and database logic now use MediaPipe landmarks, making the app easier to run and maintain (no dlib dependency).
- Registration and matching flows are updated to use face mesh data (stored as JSON in the database).
- All legacy dlib/face_encoding code and dependencies have been removed.
- The database schema now expects a `face_mesh` column (string/JSON) for facial features.
- The app is compatible with Python 3.12+ and the latest Streamlit.

### Features
- User authentication (with hashed passwords, Streamlit Authenticator)
- Register new missing person cases (with image upload and face mesh extraction)
- Public/mobile submission of potential matches
- Case matching using face mesh features
- Admin/user dashboard for case management


## How to Run

1. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/gaganmanku96/Finding-missing-person-using-AI.git
   cd Finding-missing-person-using-AI
   pip install -r requirements.txt
   ```
2. Run the main web app:
   ```bash
   streamlit run Home.py
   ```
3. To use the mobile/public submission app:
   ```bash
   streamlit run mobile_app.py
   ```

- The database will auto-create on first run (SQLite, file: `sqlite_database.db`).
- Images are stored in the `resources/` folder.

> **Note:** If you previously used the dlib version, delete any old database files and images, as the schema and features have changed.

## What is left?
 - [x] Login (Authentication)
 - [x] Submit new case
 - [x] Mobile Application (to submit user photos)
 - [ ] View submitted cases
 - [ ] View confirmed cases
 - [ ] Unit tests
 

## Developer:
## <a href="https://www.linkedin.com/in/gaganmanku96/">Gagandeep Singh</a>
## Endorse me at LinkedIn if this project was helpful. [![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn](https://www.linkedin.com/in/gaganmanku96/)


## Vote of Thanks
- Thanks to [Davis King](https://github.com/davisking) for creating dlib and for providing the trained facial feature
  detection and face encoding models used in this project.
- Thanks to the [MediaPipe](https://mediapipe.dev/) team for their open-source face mesh solution, now powering this project!
