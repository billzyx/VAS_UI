# VAS Tool Box

Welcome to the VAS Tool Box! This application allows you to download, visualize, and label voice assistant commands from Amazon Alexa.

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Features](#features)
- [Usage](#usage)
  * [Data Downloading](#data-downloading)
  * [Data Visualization](#data-visualization)
  * [Labelling](#labelling)
- [FAQs](#faqs)

## Introduction

The app is useful for extracting VAS commands for a specific time period and the user can download them and store them in a .txt or a .cha file. They can then view the data, play the commands and also download the data and label the data according to their usefulness.

## Requirements

See requirements.txt

## Features

- To get started with downloading, you will need to provide your account and password information, as well as specify the time range you want to download data from. Once the download is complete, the commands will be saved to a .txt file and a list of audio files.

- To visualize the commands, simply specify the location of the files and you will be able to see and play them.

- To label the commands, open the file for labeling and play and label the commands one by one. You can also play the whole session and check the labeling. When you are finished, don't forget to save the session.

## Usage

### Data Downloading

The goal of this task is to download the commands from your Amazon Alexa account within a specific time range.

1. Set the voice assistant account information:
   1. Click "add account."
   2. Enter your account email and password.
   3. Optionally, enter the device name.
   4. Click "save."
   
2. Set the voice assistant session information, including the session name and date time range:
   1. Click "add session."
   2. Select the desired time range for the session.
   3. Optionally, enter a name for the session.
   4. Click "save."

3. Start the data download:
   1. Click "start downloading."
   2. If prompted, enter the verification code in the browser.
   3. Wait for the download to complete.


### Data Visualization

The goal of this task is to display the downloaded data.

1. Specify the location of the data:
   1. Click "open data."
   2. Select the location of the data.
   3. Click "open."
   
2. Visualize and play the data:
   1. Optionally, click "play" to listen to the entire session.
   2. Optionally, click "play" to listen to individual commands.

### Labelling

The goal of this task is to delete useless commands (e.g., example commands provided by the voice assistant) and label error commands (e.g., commands that the voice assistant fails to recognize).

1. Open the raw data
   1. Click "open data"
   2. Select a location
   3. Click "open"
2. Check and play the commands one by one
   1. Click "Play" for a command (optional)
   2. Check if it is a useless command and label it
      1. Click the checkbox for useless commands (optional)
   3. Check if it is an error command and label it
      1. Click the checkbox for the error command (optional)
   4. Loop until finish all the commands
3. Play the commands one by one and check if the labeling is correct
   1. Click "Play" for the whole section
   2. While playing, check if the labeling is correct
4. Save the labeled data to a directory
   1. Click "save & export"
   2. Select save location
   3. Click "save"

## FAQs

- Q. Who can use this application?
  A. Anyone who owns or has an Alexa device can use this application to download and process the data that they have given to the device.

- Q. Can I, a regular user do the task of labeling?
  A. Unfortunately, only users doing research work has to access to the labeling section as it can be confusing to regular users.

- Q. Can I save the downloaded data in a pdf file?
  A. Unfortunately, you can only save data in two file formats, the .txt or the .cha format in order to visualize or label the data.

- Q. Can I save the transcripts to any custom folder on my system?
  A. Yes, you can save the data to any folder you want on your system by clicking on the "Save" button and then specifying the directory where you want your data to get saved.