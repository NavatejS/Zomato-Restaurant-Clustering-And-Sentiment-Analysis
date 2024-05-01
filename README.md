# Zomato-Restaurant-Clustering-And-Sentiment-Analysis

The project focuses on leveraging unsupervised machine learning techniques, specifically clustering and sentiment analysis, to analyze Zomato restaurant data in various cities. With the aim of benefiting both customers and the company, the analysis seeks to provide actionable insights through visualizations. By examining customer reviews and restaurant attributes, the project aims to cluster restaurants into segments and gauge customer sentiments towards them. Through this analysis, the project aims to assist customers in finding the best restaurants in their locality while enabling the company to identify areas for growth and improvement in its service offerings. Ultimately, the project aims to contribute to enhancing the overall dining experience and business operations within the Indian food industry.

The dataset consists of Zomato restaurant data, focusing on customer reviews and company insights. It includes information on menus, reviews, and delivery options. The project aims to analyze sentiments from customer reviews, visualize data for insights, and cluster restaurants into segments. Key aspects include cuisine variety, cost analysis, and identifying industry critics through reviewer metadata.

The above dataset has 10000 rows and 12 columns. There are some missing values and 36 duplicates in dataset.


### **Variables Description:**

Name: name of restaurants
Links: URL Links of the restaurant
Cost: Per person estimated cost of dining
Collections: Tagging of restaurants
Cuisines: Cuisines served by the restaurant
Timings: Restaurant timings
Reviewer: Name of the reviewer
Review: Review text
Rating: Rating provided
Metadata: Metadata of the reviewer
Time: Date and time of the review
Pictures: Number of pictures posted with the review

### **To prepare the Zomato restaurant data for analysis, several preprocessing steps were performed:**

Converted object columns to lowercase to ensure uniformity.
Removed duplicate rows and missing values to clean the dataset.
Extracted numerical values from the 'Metadata' column to create 'n_review' and 'n_follow' columns.
Processed 'Cuisines' and 'Collections' columns to remove 'nan' values, split strings into lists, and sort them.
Dropped unnecessary columns such as 'Metadata', 'Timings', 'Time', 'Links', and 'Reviewer'.
Converted 'Rating', 'n_review', and 'n_follow' columns to appropriate data types (float and integer).
Replaced 'Like' ratings in the 'Rating' column with the average rating of 3.5.
