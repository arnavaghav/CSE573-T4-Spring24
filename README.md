# CSE573-T4-Spring24

- Group #4
- Project #22: Dark Web Crawling
- Group Members:
  - Arnav Aghav
  - Rachel Guzman
  - Yang Husurianto
  - Yumi Lamansky
  - Saidubabu Mallela
  - Wangyang Ying


Abstract — Scraping the Dark Web involves extracting data from hidden online platforms that are not indexed by traditional search engines. The Dark Web is often associated with and used in the context of criminal activity due to its user anonymity and privacy features. Due to its hidden nature and extra hurdles needed to go through to reach the Dark Web compared to the worldwide web, crawling of the Dark Web allows for a glimpse into what occurs. Crawling of the Dark Web enables the extraction of information and the ability to index it for future retrieval and data analysis. In this project, we crawl the Dark Web, extract its data, and index its contents. We offer a user-friendly interface with search capabilities to examine the most recent information collected from the Dark Web.

## Apache Solr
Instructions to setup the Apache Solr server will be for Windows.

### Prerequesites
- Java 8 or greater
- `JAVA_HOME` path set to the root Java installation folder. 
  - NOTE: This is not the `java\bin` folder.
  - How to: https://confluence.atlassian.com/doc/setting-the-java_home-variable-in-windows-8895.html
  
To start the Apache Solr server:  
```
./bin/solr start -e cloud
```
This will prompt configuration options. For the purpose of this project and demonstration, one node, one shard, and one replica on the default port will be sufficient. Use the default configuration for collections.

### Indexing Data
Apache Solr will index data through the following command:
```
java -jar -Dc=<collection_name> -Dauto post.jar <path_to_data>
```
NOTE: `post.jar` has been moved for simplicity, a default installation of Apache Solr will have a path of `example\exampledocs\post.jar`.

The data should now be queryable through any REST query or viewable through: http://localhost:8983/solr
