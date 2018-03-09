# Trail Quest - Get Trekkin'

Trail Quest takes the analysis paralysis out of selecting your next hike. Using the Google Maps and Hiking Project APIs, users can specify their location and hike preferences and see a tailored list of trails near them. Users can select hikes they want to go on and save them to their profile. When users are ready to get trekkin', they can send directions to their mobile devices using the Twilio API. After completing trails, users are awarded badges. What gets you the Whistle Pig badge? Hit the trails to find out.

## The Run Down & The Tech Stack

Trail Quest uses Python for the back-end server on a Flask template and interacts with a PostgreSQL database. The homepage passes serialized data to the backend via an AJAX request to collect user preferences for trails. The Google Maps API takes the requested city/state and creates a lat/long coordinate for use by the Hiking Project API. The Hiking Project API then returns all the trails within the distance range specified by the user. All the returned trails are added to the database. The trail list is parsed by python functions that filter for distance and trail difficulty and the resulting trail objects are presented on a dynamic Google Map with info windows. The info windows have a click through link to see more information and pictures from the trail. Users can send trail head directions to their phone via the Twilio API when they are ready to get trekkin'.

The PostgreSQL database allows for users to add trails to their database to save for later. When trails are completed, users are assigned badges for the type of trail they went on, sights they may have seen, and the number of hikes they've logged.

Selenium is used for end-to-end testing with a current coverage of [  ]%

### Prerequisites

A requirements.txt file is included within the GitHub repository to make installation a breeze.

Technical savvy in Python, JavaScript, pip installation, and Selenium is encouraged before collaborating.

### Installing

A step by step series of examples that tell you have to get a development env running

#### Git Clone! (1)
Go to [GitHub](https://github.com/sarah-young/Trail-Quest-1.0/)
Clone the repo into while in your directory.
![GitHub Clone](/readme-files/01-gitclone]

`git clone https://github.com/sarah-young/Trail-Quest-1.0/`

#### Create Your Environment (2)

Check out [Virtualenv](https://virtualenv.pypa.io/en/stable/)
To set up your environment: (step 1; do this once)
`virtualenv env`

To open your environment: (step 2; do this when you start up a new terminal session)
`source env/bin/activate`

#### Pip Install (3)
If you've already downloaded Python 2 or 3, you have pip installed on your computer.
`pip install -r requirements.txt`

#### Running Trail Quest (4)
`python server.py`

#### A Quick Demo (5)

<a href="https://youtu.be/mXeGiV-I-nM"><img src="/readme-files/youtubescreenshot.jpg"
alt="Trail Quest Demo" width="240" height="180" border="10"/></a>

## Running the tests

Tests are run using Selenium.

### Break down into end to end tests

Explain what these tests test and why

`Give an example`

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With
[Atom](https://atom.io/)

## Authors

* **Sarah Young** - *Initial work* - [Trail Quest](https://github.com/sarah-young/Trail-Quest-1.0)

## Acknowledgments

* [Hiking Project](https://www.hikingproject.com/data)
Thanks to the Hiking Project for providing great trail data.

* Icons by [freepik](https://www.flaticon.com/authors/freepik)
Badge icons by freepik
