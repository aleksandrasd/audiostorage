

# Intro

An audio storage app.  

Features: 

* upload audio and video files; 
* all uploaded media automatically converted to wav/mp3;
* full text search over file names.


# How to run

Pull repository:

```bash
git clone git@github.com:aleksandrasd/audiostorage.git audiostorage
```

Build and run app

```bash
cd audiostorage
make build run
```

Open app on: http://127.0.0.1:8000/

Object storage (minio) browser: http://127.0.0.1:9001 (psw/user: minioadmin)

Postgres database: localhost:5432 (login: postgres, psw: mysecretpassword)