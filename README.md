
# Spotify Playlist Music Recommendation System

![Spotify Playlist Music Recommendation](https://i.imgur.com/693HVgg.png)

Music has served as a powerful form of cross-cultural connection and expression throughout history. In the digital age, millions of songs are easily accessible on various music platforms, providing a vast musical archive. However, navigating this extensive collection to find personalized and user-preferred music can be a daunting task. In response to this challenge, music recommendation systems have emerged as indispensable tools to enhance the user's music experience.

## Overview
This repository focuses on the design and implementation of a music recommendation system, specifically examining and evaluating the performance of a playlist recommendation system.  The system is developed using data extracted from Spotify playlists contributed by users. The study employs the K-Means clustering technique to analyze and present the results.
Also this project aims to deepen the understanding of developing music recommendation systems and make the music discovery process more effective and enjoyable for users. The ultimate goal is to establish a playlist recommendation system, allowing users to discover songs similar to those in their own playlists.

## Features
- Personalized playlist recommendations based on user's playlist songs and preferences.
- Utilizes clustering algorithms and data mining techniques to find exact match of their playlist essence
- Detailed examination of key steps including dataset cleaning, feature engineering, and clustering techniques.
- Presentation of results obtained through the K-Means clustering technique.

## Dataset of the Recommendation System
The dataset used for the Spotify recommendation system (titled data4.csv) comprises over 2.26 million tracks from the years 1921 to 2020 available on Spotify. The data, inspired by the Spotify Millions Playlist and collected by Kaggle user Sara Babu, was obtained from the Spotify Web API and through scraping methods, then organized into a tabular format. Each row in the dataset corresponds to a track, with columns containing features such as URI, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, duration_ms, popularity, and release_date. Throughout the study, essential variables like name and artists that were initially missing in the dataset have been filled, and additional features have been made available, ensuring the dataset is in its optimal form. To ensure the reliability of the study, the Spotify Millions dataset, Yamaç Eren Ay's Spotify dataset, and Jefin Paul's 170k Spotify dataset studies have been utilized during testing.

The playlist used for recommendation creation in the study: [Spotify Playlist](https://link-url-here.org)

## Data Cleaning

All details regarding dataset cleaning and preparation for application are covered in the Jupyter notebook file named [data_cleaning.ipynb](https://github.com/waldvoid/spotifyProject/blob/main/spotify_project/data_cleaning.ipynb)

## Model

All details regarding recommendation model for application are covered in the Jupyter notebook file named [model.ipynb](https://github.com/waldvoid/spotifyProject/blob/main/spotify_project/model.ipynb)

## Start Using Web Application
A user-friendly web interface has been developed using Django with Python on the backend, and HTML, CSS, and JavaScript on the frontend. The aim is to provide users with an easy way to receive quick recommendations by inputting their Spotify playlists. Through the web application, users have the opportunity to enter a Spotify playlist link. Once entered, the songs in the playlist are analyzed in the background using the K-Means clustering algorithm and cosine similarity measurement. Based on the user's listening preferences, songs from similar playlists are identified. Users can visually view these recommendations on the interface and click on the Spotify link to listen to the desired songs.

To clone the repository from GitHub to your computer and start using this project, follow these step-by-step instructions:

### Step 1: Open Git Bash or Terminal
Open Git Bash on Windows or Terminal on Mac/Linux.

### Step 2: Clone Command
Paste the following command into Git Bash or Terminal:

`git clone https://github.com/waldvoid/spotifyProject.git`

### Step 3: Navigate to Project Directory
Use the following command to navigate to the downloaded repository's directory:

`cd spotifyProject`

### Step 4: Run the Project
Install the necessary dependencies to run the project:

`pip install -r requirements.txt`

Navigate to the application directory and start the Django application:

```
cd spotify_project

python manage.py runserver
```

### Step 5: Check in the Browser
1. Open Spotify and right-click on a playlist for which you want to receive similar playlist recommendations, then choose "Copy Playlist Link."

2. Open your browser and go to "http://127.0.0.1:8000/recommend_playlist_form/."

3. If the project appears, paste the copied playlist link into the relevant field.

4. Depending on the size of your playlist, you may need to wait some time while the playlist is being prepared.
![Imgur](https://i.imgur.com/X61CwlU.png)
5. View the playlist recommendation, and if you wish to listen, click on the play button on the right to visit the Spotify address and listen.


## RESULTS
#### Python Results
As a consistent outcome of the study, the same calculated playlist is recommended to users consistently for identical inputs. For each song in the playlist, the code structure recommends 4 different songs.

Out of 400 songs, 256 songs are selected from cluster_2 (64%), 96 songs from cluster_0 (24%), and 48 songs from cluster_1 (12%).

Silhouette Score, varying between -1 and +1:
- Silhouette Score (User Playlist): 0.04446459347820573
- Overall Silhouette Score: 0.2524604748574124

According to clustering results, while cluster_2 represents a large cluster, cluster_0 and cluster_1 are divided into smaller clusters.

Silhouette scores are generally close to 0 but not very high. This indicates that the clustering model is successful in separating data points distinctly or creating homogeneous clusters.

*Clustered Spotify Dataset*
![Spotify Dataset](https://i.imgur.com/hEFFFPz.png)
*Clustered Input Playlist* *&* *Recommended Playlist*
![Input Playlist and Recommended Playlist](https://i.imgur.com/oH1LAGN.png)
#### RapidMiner Results
As a consistent outcome of the study, the same calculated playlist is recommended to users consistently for identical inputs. For each song in the playlist, the code structure recommends 1 different song.

Upon examining the RapidMiner results, it is observed that it is divided into 3 clusters, selecting 80 songs from cluster_2 (80%), 13 songs from cluster_0 (13%), and 7 songs from cluster_1 (7%) out of 100 songs.

Distances specified as:
- Avg. Within Centroid Distance: 0.101
- Avg. Within Centroid Distance Cluster_0: 0.103
- Avg. Within Centroid Distance Cluster_1: 0.075
- Avg. Within Centroid Distance Cluster_2: 0.105

According to RapidMiner results, while cluster_2 represents a large cluster, cluster_0 and cluster_1 are divided into smaller clusters.
We should use Avg. Within Centroid Distance values to evaluate the homogeneity within clusters. The Avg. Within Centroid Distance value is a metric that measures the similarity or homogeneity of data points within each cluster in the clustering model. A low Avg. Within Centroid Distance value indicates that data points within a cluster are close to each other, and this cluster is more homogeneous. Although the overall values indicate that the clusters are homogeneously distributed, especially the lower value of cluster_1 compared to other clusters indicates that the data points within cluster_1 are closer and more homogeneous.

