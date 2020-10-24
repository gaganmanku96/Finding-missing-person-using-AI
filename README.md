# Find Missing Person using AI

Hundreds of people (especially children go missing every day) in India. There are various <b>NGO's and Govt Initiatives</b> to help with it. This project tries to implement an  existing/new way to help.

## News Articles
#### [Article 1](https://www.thehindu.com/society/indias-missing-children-what-the-whatsapp-rumours-dont-tell-you/article24641527.ece)
![News Article 1](resources/news_1.PNG)
#### [Article 2](https://www.deccanchronicle.com/nation/current-affairs/250518/indias-children-174-go-missing-every-day-half-untraced.html)
![News Article 2](resources/news_2.PNG)


## What is the objective of this Project and how will it help?
The objective of this project is to help Police and higher authorities to track down missing people quickly. The usual process to track a person is using investigation which requires time and experience (to ask right questions). Most of the time, investigation method works pretty well but it is time consuming and can be unsuccessful if the person (missing) has been shifted/moved to different location (city/country).<br>
In such cases, the ideal approach is to go through CCTV footages and evidences. Again, this can be very time consuming and given the number of people that go missing everyday, it can be a challanage to keep up with it.<br>

## Solution (Project's Implementation)
### 1. Registering New Cases
The first step is to register a new case. The GUI application is built using <b>PyQT5</b> that allows you to collect all relevant information and store it in database <b>Postgres</b>.
> Please ignore the SRK's image. It is just for the sake of project :)

![New Case Window](resources/new_case.PNG)

### 2. Waiting for Users to submit images
So far we have only talked about 'how new cases will be registered', the next thing we have to do is to match these registered cases but who do we match it with? This is where ours Users come in. These users are common people like you and me who wants to make a change in the society.<br>
The common people will use an application on their mobile to submit photos of people who they think have lost or found begging while keeping them their identity anonymous. The anonymous part is very important because they fear of local <i>Gundas</i> that might create trouble for them.<br>
> Mobile Application
![Mobile Application](resources/mobile_application.PNG)

> An android Application can also be build and used but I have very little experience in it.
### 3. Matching Cases
The next step is to match the case images and user submitted images. To match <b>KNN Algorithm </b> is used.
![Main Application](resources/app_window.PNG)

## Installation
