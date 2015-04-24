# talons
A web scraper using the [Falcon](http://falconframework.org/) framework.

Data is submitted using the RESTful API. Requests for new pages to scrap are made through ```POST``` and resulting data is given through ```GET```. HTTP status codes are used to reference how the server responded to your request. All response data is JSON formatted.

It is recommended that you run this with [```gunicorn```](http://gunicorn.org/).

#### Routes, parameters, and responses

##### ```POST /addjob```
- ```url``` - The URL that you want to scrap
- Responses
  - ```200 OK``` - This means that your job was created successfully. The response data will contain a ```job-id``` which should be used for future reference to get the results of the scrap.
  - ```400 Bad Request``` - The URL parameter was not given in the request made.

##### ```GET /job/{job-id}```
- ```job-id``` - The job ID associated with the job
- Responses
  - ```200 OK``` - This is the only response possible, but there are two possible outcomes:
    - Response data contains ```status```. This means that your job is still processing. ```status``` can be either ```IN_PROGRESS``` or ```INCOMPLETE```.
    - Response data contains ```result```. This means your job has completed and the web page was scraped successfully, with the response of that webpage returned as ```result``` in the response from talons.

#### Example run

    $ gunicorn scraper
    
    $ http --form POST http://localhost:8000/addjob url='http://www.google.com/'
    HTTP/1.1 200 OK
    Connection: close
    Date: Fri, 24 Apr 2015 21:24:36 GMT
    Server: gunicorn/19.3.0
    content-length: 66
    content-type: application/json; charset=utf-8
    
    {
        "error": false, 
        "job-id": "ea9aa33d-8661-4d99-8233-093137abf30c"
    }
    
    $ http GET http://localhost:8000/job/ea9aa33d-8661-4d99-8233-093137abf30c
    HTTP/1.1 200 OK                                                                                       
    Connection: close                                                                                     
    Date: Fri, 24 Apr 2015 21:25:55 GMT                                                                   
    Server: gunicorn/19.3.0                                                                               
    content-length: 18428                                                                                 
    content-type: application/json; charset=utf-8                                                         
    
    {                                                                                                     
        "error": false,                                                                                   
        "result": "<!doctype html> ..."
    }
    
