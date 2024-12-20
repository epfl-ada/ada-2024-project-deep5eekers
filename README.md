# Exploring Gender Dynamics in Film

## Abstract

In this project we will explore the role of gender in the film industry. We have decided to investigate a variety of ideas and themes around gender. We will consider questions about gender in roles, directors, character portrayals, and general sentiment. 

We were inspired to choose this topic because gender representation in film provides a lot of insight into how the world/region portrays gender roles. With our data story, we will investigate the potential gender imbalances and stereotypes present in films over time. We will effectively show any disproportionly representation in film. We will show the possible character stereotypes that are damaging to our view of women. Also, we will look into the general sentiment associated with men and women characters. Exploring these topics will bring to light the potential misrepresentations and imbalances of gender in film. We feel that creating this story is important because of this.

## Research Questions

In this section we have listed the main research questions we would like to address during this project. 

- RQ1: What gender imbalances exist in acting roles, and how do these differences vary over time, across genres, and between countries?
- RQ2: What stereotypical character types are associated with each gender?
- RQ3: In plot lines, are male and female characters typically assigned different actions and portrayals? Do the words used in each case convey positive or negative connotations?
- RQ4: Is unequal gender representation in films linked to a movie’s success or failure? Are Oscar nominations balanced across genders?
- RQ5: Does gender inequality exist in production roles as well? Does a director's gender influence the portrayal of male and female characters in films?

In addition to these main questions, we may choose to explore other sub-questions. As we have gone through the dataset in our initial analysis, we have stumbled upon other interesting gender-related topics. For example, we may look into how movie ratings differ for movies with female leads versus male leads. 

## Supplementary Data

- Wikipedia: In addition to the CMU dataset, we are using the Wikipedia pages that exist for a subset of the CMU dataset movies. We are going to use this Wikipedia pages for several purposes: retrieve plot summary information (it might be richer than provided in CMU), get IMDb id for the movies, retrieve general information about people (gender, occupation). To access the Wikipedia data, we are processing the latest wikipedia dump, using 'wiki_movie_id' key in the CMU dataset to retrieve the specific pages.  

- IMDb: We are also planning on using data from IMDb. We will access movies' scores, number of votes and the information about the people: directors, writers. We want this data for two main reasons: to study the relationship between a lead role's gender and the respective movie's IMDb rating and to study the potential gender imbalances in movie production jobs. To access this data, we used the IMDb ID which is commonly found in the Wikipedia pages. Since IMDb's API has licensing restrictions, it is not so straightforward to access the data. Instead, we are going to use IMDb's provided non-commercial datasets.  

- Oscar: We are planning to use data from the Oscar nomination to analyze gender inequality in the awards nomination. We will use public Oscar's search base and parse the provided html with award's history for our needs.  

## Methods

### Research Question 1: Gender Imbalances
The first step to starting off our analysis, was getting to know the data and the information we could gather based on that. 

- We wrote utility functions in order to load the datasets in convenient formats.
- Preliminary analysis was conducted to visualize the representation of male and female characters, across countries, years and genres. (RQ1) 
- We have used the clustering provided by the CMU datasets. Analysis of frequency of different personality traits by gender was performed. (RQ2)
- We have enriched our data with additional datasets, scrapping information from wikipedia, getting familiar with IMDb and Oscar datasets. Those datasets are merged using Wikipedia to IMDb id mapping. We still have to enrich the data, as currently no gender labels for production roles and Oscar dataset are present. 

^ simon: old info i think, below is what i write

To address RQ1, we decided to split our analysis of gender imbalances into three sections:
- Time
- Geography
- Genres

#### **Time**
We created a decade feature from the CMU dataset to count the number of male and female actors in each decade. We also visualized the ratio of male actors by year to see if that was trending in any direction. 

#### **Geography**
We expanded our search of the ratio of male actors by year to each continent. We also looked at the gender distribution difference by country to see if the data was more diverse than the by continent results. 

#### **Genres** 
We looked at the top genres by total cast data, then calculated the ratio of female cast members by genre. This data helped show what genres women were more represented in. 

### Research Question 2: Gender Stereotypes
To address RQ2, we investigated potential stereotypes with the characters of each gender, by clustering the TV tropes data by character type and gender. This gave us information about the common character types played by each gender. 

### Research Question 3: Plot Analysis
![Plot Analysis Pipeline](./data/plot_analysis_pipeline.png)

To address RQ3, we conducted a plot analysis using [the Book NLP library](https://github.com/booknlp/booknlp), which provides capabilities such as Named Entity Recognition (NER), coreference resolution, and dependency parsing. Specifically designed for literary texts, Book NLP was selected for its effectiveness in analyzing narrative structures. We identified characters' genders through pronoun-based gender recognition and analyzed words associated with each character using dependency parsing.

Expanding beyond basic word associations, we extracted events involving agent and patient roles and employed [the COMET model along with the Kogito library](https://github.com/epfl-nlp/kogito) to infer likely character attributes (xAttribute) and emotions (xReact, oReact) from these events.

Our analysis included the following components:

- **Mention / Character Count by Gender**: Counting the number and frequency of mentions for female and male characters in the plot.
- **Word Cloud by Gender**: Visualizing words associated with each gender across various roles, such as possessive words, agents, and patients.
- **Attributes and Emotion Word Cloud by Gender**: Highlighting inferred character attributes and emotions based on event analysis.


### Research Question 4: Representation & Success
To address RQ4, we investigated how gender relates to success in box office revenue and Oscar nominations. We did this by calculating the female cast ratio for each movie that had box office revenue data and visualizing that data. For the second part of the question, we used the Oscar dataset to compare nomination categories by gender balance.

### Research Question 5: Behind The Scenes 
To address RQ5, we used IMDB data to find director names from the top 10,000 rated movies and scrapped their gender from text counting mentions of pronouns (e.g. he, her, him, his, hers). Using the movies and the respective gender of the directors, we were able to get distributions of revenue, ratings, and votes for each director's gender.
## Project Timeline


### Week 1: Finalize P2 achievements
- Merge CMU, IMDb and Oscar data (Enrich collected data with Gender data for Actors, Directors, etc. using Wikipedia)
- More work on RQ1, RQ2, additional hypothesis testing
- In depth work on RQ3
### Week 2: Homework  
- Start working on RQ5
- ADA Homework 2 =) 
### Week 3: Oscar and Revenue
- Work on RQ4, evaluating box office and gender associations
- Analyze Oscar data, enhance analysis of the (RQ5) with more production roles from the Oscar data. 
### Week 4: Data Visualization
- Start working on the website
- Work on detailed/rich visualizations (matplotlib plots --> JS plots)
### Week 5: Final Presentation
- Write a story, project presentation
- Clean up visualization


### Deep5eekers Team

- Simon Anton (WebDevelopment expert)
- Kyuhee Kim (Plot Analysis expert, RQ3)
- Christina Kopidaki (Visualization expert, RQ1, RQ2)
- Margarita Mikhelson (Statistician, Hypothesis testing)
- Ivan Pavlov (Data Engineer, Enriching the data)
