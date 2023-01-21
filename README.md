# Cassandra Sparkify project
## Introduction
This project is about a fictional startup, Sparkify. It has developed a new music streaming app and wants to analyse the data they've been collecting about songs and user activity. 

The analytics team is particularly interested in understanding which songs users are listening to. However, there is currently no easy way to interact with the data, since it's in a directory of csv files. 

The aim is to create an Apache Cassandra database which can query this song data. The team has already planned the queries they'd like to run. 

This project involves writing a small ETL pipeline in Python and designing a data model in Apache Cassandra. The pipeline will transform the data from several csv files into a single, streamlined file. This data will then be modelled and inserted into Apache Cassandra tables.

## Dataset
This project involves an `event_data` dataset. It's initially a directory of csv files, with each file representing a day. Example filepaths look like

`event_data/2018-11-08-events.csv`
`event_data/2018-11-09-events.csv`
