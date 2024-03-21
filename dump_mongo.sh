#!/bin/bash
mongodump --uri="mongodb://localhost:27017" --db=cpsync --out=./dump
