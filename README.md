## Run
```
docker compose up -d --build
```


## Performance Test
Modify ```redirect_load.js``` and then:
``` 
docker compose run --rm k6 run /app/tests/performance/redirect_load.js
```