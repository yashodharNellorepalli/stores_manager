Schema

connect to the cluster --> mongodb+srv://yash:yashmongodb@cluster0.osxq8.mongodb.net/stores_master?retryWrites=true&w=majority
Or create your own cluster


stores --> load the data from https://drive.google.com/file/d/1dCdAFEBzN1LVUUKxIZyewOeYx42PtEzb/view?usp=sharing
images --> storage of images and its info like height, width
store_visits -> straight insertion of /api/submit data into this collection

commands:
virtualenv -p python3 vEnv (creating virtualEnv)
source vEnv/bin/activate (get into the environment)
pip3 install -r requirements.pip (install packages)
install redis and up the redis server

CELERY 
celery -A app.celery.tasks worker --pool=solo --loglevel=info

Testing:
run tests/test.py

Tools: IntelliJ IDE

More Time: Authorization, module of request args check of datatype and dat range if any

NOTE: Please add the data to env.cfg file if you want to change the config

CURL:
curl --location --request GET 'http://localhost:8081/stores/api/status?job_id=5f8702ad0e740b389f4a5ebb'

curl --location --request GET 'http://localhost:8081/stores/api/visits?area=710006&store=S00339218&startdate=2020-10-10&enddate=2020-10-20'

curl --location --request POST 'http://localhost:8081/stores/api/submit' \
--header 'Content-Type: application/json' \
--data-raw '{
   "count":2,
   "visits":[
      {
         "store_id":"S00339218",
         "image_url":[
            "https://www.gstatic.com/webp/gallery/4.jpg",
            "https://www.gstatic.com/webp/gallery/5.jpg"
         ],
         "visit_time": "2020-10-10 10:00:00"
      },
      {
         "store_id":"S00339204",
         "image_url":[
            "https://www.gstatic.com/webp/gallery/1.jpg"
         ],
         "visit_time": "2020-10-10 10:00:00"
      }
   ]
}'