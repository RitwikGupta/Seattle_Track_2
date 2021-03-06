# Challenge 1: Identifying COLREGs Interactions 

Out of the millions of data points in the AIS dataset can you find the most efficient algorithm to identify potential collisions? 

COLREGs interactions are defined by situations where there are constant bearing and decreasing range between two ships. In other words, two ships are headed for collision unless one or both change course or speed. COLREGs also assume that two ships are visually in sight of one another. You can assume they are a maximum of 4 nautical miles away. This challenge is about developing a screening tool for ships interactions within an AIS dataset, which is akin to finding the proverbial needle in the haystack. 

As a starting point, consider looking for places where ships operate with a higher than average risk of collision. Ships frequently come close to each other in high traffic areas, like port entrances, but often the ships are not moving, or the interactions are governed by prescriptive criteria, like traffic lanes. The more interesting interactions are in areas where the traffic patterns have not explicitly defined. 

You may use any of the AIS data to address this challenge, but we would suggest looking at a high traffic area with rules, like the Los Angeles/San Diego area (UTM 11) and an area that has less rules and more open ocean, like The Caribbean (UTM 17 and 18, less than 27 degrees latitude), as a starting point we have pre-loaded some data into the ESRI platform and the GitHub repository.  

The judging criteria for the challenge will include: 
Up to 50 points for developing a computationally efficient screening tool. We need a way to go from millions of data point to the few hundred thousand that might represent interesting interactions between ships. There are a couple of examples of approaches in the GitHub repository, but none are efficient enough to handle the size and scale of the full AIS dataset.

Up to 40 points for techniques to refine the initial screening tool. Once we have a screening tool, we need to go from hundreds of thousands of candidates to those that are actually COLREGs interactions. The candidate interactions might include activities like towing or ships in port that need to be filtered out. In some cases, the 1-minute intervals in the Marinecadstre dataset will not be sufficient to capture the nuances of the interaction and identification will require linking to another dataset, like Spire, to get the ships’ tracks. We prefiltered the Jan 2106 UTM 11 (LA/San Diego) dataset by proximity (4 nautical miles) if you want to use that as a starting point.  From there you can refine your algorithms in any way you see fit. 

Up to 10 points for data presentation and visualization.

