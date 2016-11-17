### Project Description ###

This is a program that builds a graph out of a large sampling of data and performs various operations on that graph as commanded by the user. These functions will work on any arbitrary graph, but this project and all testing done on it is oriented toward web graphs. A large sampling of data is already provided in the 'data' folder. The data provided is a small sub-graph of the full web to allow faster development and testing, though the graph is still fairly large.

The nodes file gives the mapping of url to id ("buffalo.edu\t6136198") and the edges file gives every edge by the node id's in the order of source node then destination node ("15328636\t6136198"). This edge means that site "15328636" contains a link to site "6136198". 

Data sources: The data was obtained from http://webdatacommons.org/hyperlinkgraph/2012-08/download.html which was extracted from Common Crawl (http://commoncrawl.org/). To reduce the size of the graphs, we use the pay-level-domain graph that has been filtered to only include the most popular sites according to Alexa (http://s3.amazonaws.com/alexa-static/top-1m.csv.zip). The data has been filtered down to 101,797 sites connected by 8,303,699 hyperlinks. Note that the graph is from 2012 so many newer sites will not be present.

### How do I get set up? ###

This program is run from the command line using python. 

The various operations that can be performed on the graph are Prune, Path, and Cover. Here is how to use each.

**Prune**

```
#!python

python WebGraph.py -prune nodeFilename edgeFilename outputFilename k
```
Returns a graph containing only sites with *k* or more sites linking to it. The returned graph can contain sites with fewer than k incoming edges as long as they had k or more links in the original graph.

Creates a file with the name contained in the *outputFilename* parameter with the edges of the new graph in the same format as the input edges file.

*nodeFilename* is the path to the nodes file. By default this is data/nodes.

*edgeFilename* is the path to the edges file. By default this is data/edges.

**Path**

```
#!python

python WebGraph.py -path nodeFilename edgeFilename outputFilename startURL destinationURL
```
Writes the edges into the output file of the shortest path from startURL to destinationURL. Ties in distance between multiple paths are broken arbitrarily. 

Creates a file named *outputFilename*. The format of the output is a list of edges by domain name (not node id) in the order of the path.

Note that we are working with pay level domains so this is not the minimum number of clicks to get from one site to another, but it is the shortest domain name path.

**Cover**

```
#!python

python WebGraph.py -cover nodeFilename edgeFilename outputFilename k url
```
Given a domain name, removes it from existence! In addition to removing the given url from the web graph, the program also removes any site linking to the domain with distance k or less.

Creates a file named *outputFilename* with the edges of the new graph in the same format as the input edges file.

*
Project completed for Jesse Hartloff's CSE 250*