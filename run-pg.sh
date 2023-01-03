docker container rm -f flagops-postgres
docker run --name flagops-postgres --network=host -e POSTGRES_USER=flagopsuser -e POSTGRES_PASSWORD=password -e POSTGRES_DB=flagopsdb -d postgres:14
