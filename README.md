# Gender in the Film World

## Abstract

In this project we will explore the role of gender in the film industry. We have decided to investigate a variety of ideas and themes around gender. We will consider questions about gender in roles, directors, character portrayals, and general sentiment. 

We were inspired to choose this topic because gender representation in film provides a lot of insight into how the world/region portrays gender roles. With our data story, we will investigate the potential gender imbalances and stereotypes present in films over time. We will effectively show any disproportionly representation in film. We will show the possible character stereotypes that are damaging to our view of women. Also, we will look into the general sentiment associated with men and women characters. Exploring these topics will bring to light the potential misrepresentations and imbalances of gender in film. We feel that creating this story is important because of this.

## Research Questions

In this section we have listed the main research questions we would like to address during this project. 

- What gender imbalances exist in acting roles, and how do these differences vary over time, across genres, and between countries?
- What stereotypical character types are associated with each gender?
- In plotlines, are male and female characters typically assigned different actions and portrayals? Do the words used in each case convey positive or negative connotations?
- Is unequal gender representation in films linked to a movie’s success or failure?
- Does gender inequality exist in production roles as well? Does a director's gender influence the portrayal of male and female characters in films?

In addition to these main questions, we may choose to explore other sub-questions. As we have gone through the dataset in our initial analysis, we have stumbled upon other interesting gender-related topics. For example, we may look into how movie ratings differ for movies with female leads versus male leads. 

## Supplementary Data

- Wikipedia: In addition to the CMU dataset, we are using the Wikipedia pages that exist for a subset of the CMU dataset movies. We are going to use this Wikipedia pages for several purposes: retrieve plot summary information (it might be richer than provided in CMU), get IMDb id for the movies, retrieve general information about people (gender, occupation). To access the Wikipedia data, we are processing the latest wikipedia dump, using 'wiki_movie_id' key in the CMU dataset to retrieve the specific pages.  

- IMDb: We are also planning on using data from IMDb. We will access movies' scores, number of votes and the information about the people: directors, writers. We want this data for two main reasons: to study the relationship between a lead role's gender and the respective movie's IMDb rating and to study the potential gender imbalances in movie production jobs. To access this data, we used the IMDb ID which is commonly found in the Wikipedia pages. Since IMDb's API has licensing restrictions, it is not so straightforward to access the data. Instead, we are going to use IMDb's provided non-commercial datasets.  

- Oscar: We are planning to use data from the Oscar nomination to analyze gender inequality in the awards nomination. We will use public Oscar's search base and parse the provided html with award's history for our needs.  

## Methods

### Part 1: Getting familiar with the data.
The first step to starting off our analysis, was getting to know the data and the information we could gather based on that. 

*Step 1:* We wrote utility functions in order to load the datasets in convenient formats.

*Step 2:* Preliminary analysis was conducted to visualize the representation of male and female characters, across countries, years and grenres.

### Plot Analysis

![Plot Analysis Pipeline](plot_pipeline.png)

For our plot analysis, we used [the Book NLP library](https://github.com/booknlp/booknlp) to perform Named Entity Recognition (NER), coreference resolution, and dependency parsing. Book NLP, specifically designed for literary texts, was chosen as it is well-suited for analyzing narrative structures like plots. We identified characters' genders through pronoun-based Gender Recognition and examined words associated with each character using dependency parsing.

Our analysis included:

- Counting the number and mention frequency of female and male characters in the plot ("Mention Count by Gender"), and
- Examining words associated with each gender in different roles, such as possessive words, agent words, patient words, and modifiers ("Word Cloud by Gender").

Moving beyond simple word associations, we extracted events related to agent and patient words, using the COMET model to infer potential character attributes (xAttribute) and emotions (xReact, oReact) based on these events. This allowed us to analyze variations in personas and emotional responses across genders.


### ML
Train a model to predict gender from metadata (e.g., role, genre, awards). Analyze feature importance to identify attributes strongly correlated with each gender.

### Clustering of genre success (revenue) by gender

Task: That you have a reasonable plan and ideas for methods you’re going to use, giving their essential mathematical details in the notebook.

## Project Timeline


## Team Milestones


---

### Deep5eekers Team

- Simon Anton
- Kyuhee Kim
- Christina Kopidaki
- Margarita Mikhelson
- Ivan Pavlov
