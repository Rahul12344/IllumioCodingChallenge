In terms of my solution, I elected to use a Trie structure to hold the rules. The root is a
dummy node consisting of pointers to the direction. From the direction, we have pointers to
the protocols, and from the protocols, pointers to the ports, and from the ports pointers to 
the IP addresses and their associated ports in order to delineate different IP addresses. In 
addition, the way in which ports and ip addresses are stored are bucketed. Since the problem 
statement specifies that ALL port and ALL ip addresses must fall within a valid range, and 
ALL inputs are valid, we can create buckets of size 1-65535, and four separate buckets for each
integer 0-255 of the ip addresses. 

In terms of optimization, the actual lookups themselves should be fairly constant as each ip and 
port correspond to a specific bucket. However, I chose to make this tradeoff of constant lookup
for space inefficiency. Had I taken more time, I would have tried to implement a more range-based 
bucketing system that doesn't necessary facilitate the creation of the maximum number of buckets
upon instantiation. This would save space to a degree. Additionally, for both direction and protocol,
as there are only two options to choose from, I could have saved time by assigning each a specific 
position in the array of children nodes as I loop through each linearly to find the corresponding protocol
or direction.

In terms of testing, I chose to use a variety of overlapping ranges as tests because I felt like
that would be a painpoint for the algorithm. Additionally, I tested for validity at each stage,
meaning I tested for invalid direction, protocol, port, and ip_range to check if my algorithm
was valid for each stage.

In terms of my interests, I would love to work on the Data team as my first choice, with the Platform
team being a close second as I feel like those two teams align most closely with my interests.

