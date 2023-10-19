<p align="center"> 
  <img src="https://avatars.githubusercontent.com/u/95070156?s=200&v=4">
</p>

# Crossmint Coding Challenge

---
## Introduction
The goal of this challenge is to populate the Megaverse with different types of astral objects.
We are given different APIs to create such objects, and a target scenario that we have to mimic.

---
## Application
The application consist of two entrypoints, one for populating the map, and an optional one for resetting
it, which came in handy during testing, so I decided to keep it.

The app is written in Python (3.11). The entrypoints could easily have been scripts, but I decided to wrap them
around two RPC endpoints, for which I chose FastAPI as the web framework.  I also included a Dockerfile for easy local
deployment and testing.

---
## Strategy
For the target scenario to replicate, we can get the information from this endpoint: `/api/map/[candidateId]/goal`

We parse the response, run some validations, and proceed to call the corresponding endpoints to create each object.
Always keeping in mind the positional dependencies between them. In our particular case `POLYanet` should be created
before `SOLoons` and the latter should always be adjacent to a `POLYanet` (For adjacency I only checked: up, down, left, 
and right. I didn't check diagonals, but it should be trivial to add if needed).

There is a retrying policy in case of a 429 Error (Too Many Requests) when creating this objects.

---
## Running the app
I included a Dockerfile for an easy running and testing of the solution.

Building the image:
```
docker build -t cm-app .
```
Running a container:
```
docker run -d -p 80:80 cm-app
```
Populating the map:
```
curl --request POST 'http://127.0.0.1/fillMap'
```
Resetting the map:
```
curl --request POST 'http://127.0.0.1/resetMap'
```
