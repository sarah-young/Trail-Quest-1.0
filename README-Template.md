# Trail Quest

Trail Quest takes the analysis paralysis out of selecting your next hike. Using the Google Maps and Hiking Project APIs, users can specify their location and hike preferences and see a tailored list of trails near them. Users can select hikes they want to go on and save them to their profile. When users are ready to get trekkin', they can send directions to their mobile devices using the Twilio API. After completing trails, users are awarded badges. What gets you the Whistle Pig badge? Hit the trails to find out.

## The Run Down & The Tech Stack

Trail Quest uses Python for the back-end server on a Flask template and interacts with a PostgreSQL database. The homepage passes serialized data to the backend via an AJAX request. The Google Maps API takes the requested city/state and creates a lat/long coordinate for use by the Hiking Project API. The Hiking Project API then returns all the trails within the distance range specified by the user. All the returned trails are added to the database. The trail list is parsed by python functions that filter for distance and trail difficulty and the resulting trail objects are presented on a dynamic Google Map with info windows that present more information and a click through link to see pictures from the trail. Users can send trail head directions to their phone via the Twilio API.

The postgreSQL database allows for users to add trails to their database to save for later. When trails are completed, users are assigned badges for the type of trail they went on, sights they may have seen, and the number of hikes they've logged. 

Selenium is used for end-to-end testing with a current coverage of [  ]%

### Prerequisites

A requirements.txt file is included within the GitHub repository to make installation a breeze.

Technical savvy in Python, JavaScript, pip installation, and 

### Installing

A step by step series of examples that tell you have to get a development env running

Git Clone! <1>

```
Go to [GitHub](https://github.com/sarah-young/Trail-Quest-1.0 "Trail Quest GitHub Repo")
Clone the repo.
[[[ INSERT SCREENSHOTS ]]]


<!-- KEEP GOING FROM HERE -->
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

