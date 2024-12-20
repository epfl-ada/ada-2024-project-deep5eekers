# Exploring Gender Dynamics in Film

Our datastory is available in the following link: https://pavlov200912.github.io/ada-deep5eekers/

## Abstract

In this project we will explore the role of gender in the film industry. We have decided to investigate a variety of ideas and themes around gender. We will consider questions about gender in roles, directors, character portrayals, and general sentiment. 

We were inspired to choose this topic because gender representation in film provides a lot of insight into how the world/region portrays gender roles. With our data story, we will investigate the potential gender imbalances and stereotypes present in films over time. We will effectively show any disproportionly representation in film. We will show the possible character stereotypes that are damaging to our view of women. Also, we will look into the general sentiment associated with men and women characters. Exploring these topics will bring to light the potential misrepresentations and imbalances of gender in film. We feel that creating this story is important because of this.

## Research Questions

In this section we have listed the main research questions we tried to answer during this project. 

- RQ1: What gender imbalances exist in acting roles, and how do these differences vary over time, across genres, and between countries?
- RQ2: What stereotypical character types are associated with each gender?
- RQ3: In plot lines, are male and female characters typically assigned different actions and portrayals? Do the words used in each case convey positive or negative connotations?
- RQ4: Is unequal gender representation in films linked to a movie’s success or failure? Are Oscar nominations balanced across genders?
- RQ5: Does gender inequality exist in production roles as well? Does a director's gender influence the portrayal of male and female characters in films?

## Supplementary Data

- Wikipedia: In addition to the CMU dataset, we have utilized the Wikipedia pages corresponding to a subset of the CMU dataset movies. These pages were processed to retrieve plot summary information (often richer than the summaries provided in the CMU dataset), IMDb IDs for the movies, and general information about people, such as gender and occupation. To access this data, we processed the latest Wikipedia dump, leveraging the wiki_movie_id key from the CMU dataset to identify and extract the relevant pages.

- IMDb: We have extracted data from IMDb, focusing on movies' scores, number of votes, and information about people involved in production, such as directors and writers. This data helped us analyzing potential gender imbalances in movie production jobs. Using the IMDb ID obtained from the Wikipedia pages, we accessed IMDb's provided non-commercial datasets, as the official IMDb API has licensing restrictions.

- Oscar: To analyze gender inequality in Oscar nominations, we crawled data from the public Oscar awards search base. By parsing the provided HTML containing awards history, we extracted information necessary for our analysis, including nomination categories, nominees' names, and genders. This dataset allows us to explore disparities in representation among nominees across different categories.

## Methods

### Research Question 1: Gender Imbalances
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
To address RQ2, we investigated potential stereotypes with the characters of each gender, by clustering the TV tropes data by character type and gender. This gave us information about the common character types played by each gender and gave us some initial insights into bias around genders in film.

### Research Question 3: Plot Analysis
![Plot Analysis Pipeline](./data/plot_analysis_pipeline.png)

To address RQ3, we conducted a plot analysis using [the Book NLP library](https://github.com/booknlp/booknlp), which provides capabilities such as Named Entity Recognition (NER), coreference resolution, and dependency parsing. Specifically designed for literary texts, Book NLP was selected for its effectiveness in analyzing narrative structures. We identified characters' genders through pronoun-based gender recognition and analyzed words associated with each character using dependency parsing.

Expanding beyond basic word associations, we extracted events involving agent and patient roles and employed [the COMET model along with the Kogito library](https://github.com/epfl-nlp/kogito) to infer likely character attributes (xAttribute) and emotions (xReact, oReact) from these events.

Our analysis included the following components:

- **Mention / Character Count by Gender**: Counting the number and frequency of mentions for female and male characters in the plot.
- **Word Cloud by Gender**: Visualizing words associated with each gender across various roles, such as possessive words, agents, and patients.
- **Attributes and Emotion Word Cloud by Gender**: Highlighting inferred character attributes and emotions based on event analysis.


### Research Question 4: Representation & Success
To address RQ4, we explored how gender relates to success in both box office revenue and Oscar nominations. For the first part of the question, we calculated the female cast ratio for each movie that had box office revenue data and visualized the distribution to examine potential patterns. This analysis allowed us to investigate whether movies with a higher proportion of female representation in their casts tend to achieve comparable commercial success.

For the second part, we utilized an Oscar dataset that we crawled, capturing a comprehensive history of nominations and winners across categories. Our findings revealed a significant disparity: female nominees are vastly underrepresented compared to their male counterparts across most categories. This imbalance is particularly striking in fields like directing and screenplay writing, where female representation remains minimal. Even in categories traditionally considered more inclusive, such as acting awards, the proportion of female nominees still lags behind men in terms of overall recognition.

### Research Question 5: Behind The Scenes 
To address RQ5, we examined how a director’s gender influences key movie success metrics such as revenue, ratings, and votes. Using IMDB data, we identified director names from the top 10,000 highest-rated movies and employed a scraping approach to infer their gender by analyzing text for mentions of gendered pronouns (e.g., he, her, him, his, hers). This method allowed us to approximate gender representation among directors in a systematic way.

By pairing the inferred gender with the respective movies, we analyzed and visualized distributions of box office revenue, user ratings, and audience vote counts across male and female directors. Our findings revealed stark disparities: male directors overwhelmingly dominate the data, with significantly higher representation in all categories. Additionally, while movies directed by women often achieve comparable or even superior ratings, their frequency is far lower, and their revenue distributions suggest a systemic bias in resource allocation or marketing opportunities.

This analysis highlights the underrepresentation of female directors in the film industry and raises important questions about how gender dynamics shape both the opportunities available to directors and the audience reception of their work.

### Deep5eekers Team

- [Simon Anton](mailto:simon.anton@epfl.ch) (WebDevelopment and Visualization expert, StoryTeller)
- [Kyuhee Kim](mailto:kyuhee.kim@epfl.ch) (Plot Analysis expert, RQ3)
- [Christina Kopidaki](mailto:christina.kopidaki@epfl.ch) (WebDevelopment and Visualization expert, RQ1, RQ2)
- [Margarita Mikhelson](mailto:margarita.mikhelson@epfl.ch) (Statistician, Hypothesis testing, Used data extracted by plot analysis and turned them to meaningful results)
- [Ivan Pavlov](mailto:ivan.pavlov@epfl.ch) (Data Engineer, Enriching the data and using them to answer RQ4, RQ5)


- Simon Anton (WebDevelopment expert)
- Kyuhee Kim (Plot Analysis expert, RQ3)
- Christina Kopidaki (Visualization expert, RQ1, RQ2)
- Margarita Mikhelson (Statistician, Hypothesis testing)
- Ivan Pavlov (Data Engineer, Enriching the data)