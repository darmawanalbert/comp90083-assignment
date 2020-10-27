# Actionables:
1. Data Collection: Mean Travel Time (Albert)
2. Destination allocation each day based on probability (Nuvi)
3. Jupyter Notebook - BatchRunner (ongoing)
4. Jupyter Notebook - Histogram Data Distribution
5. Server.py - Legends for every agent color
6. Server.py - Print number of odd and even cars

# Notes
24 hour timeline
0 1 2 3 4 5 6 (7 8 9 10) 11 12 13 14 15 (16 17 18 19) 20 21 22 23

normal distribution

Peak hour 1 : 7-10
Peak hour 2 : 16-19

5 odd-even policy
 0  0 -> 7-10 and 16-19 (3 hour each)
+1 +1 -> 8-11 and 17-20 (3 hour each)
-1 -1 -> 6-9 and 15-18 (3 hour each)
+1 -1 -> 8-9 and 17-18 (1 hour each)
-1 +1 -> 6-10 and 15-20 (4 hour each)
1 Without

ANOVA
1 simulation = 288 seconds (20 fps in local machine) = 4.8 minutes * 30 = 144 minutes = ~2 hours

Metrics: Travel Time

7-7, 9-5 business hours

Actionables
1. Change Peak hour parameter
2. Print time