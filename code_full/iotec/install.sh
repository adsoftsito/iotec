
cd nodejs_frontend
docker build -t front_user .

cd nodejs_rest_api
docker build -t rest_user .

cd nodejs_webtoken
docker build -t token_user .


docker run -p 80:80 -d front_user
docker run -p 8081:8081 -d rest_user
docker run -p 8082:8082 -d token_user
