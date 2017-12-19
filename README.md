# Wizards-NP-Constraint-Satisfaction

We are given a list of Wizards in the form of:

Harry Hermione Snape
Hermione Dumbledore Harry

The information given shows is that the third Wizards age is not between the ages of the first two.

The algorithm uses a greedy and random solution to get out of ruts.

We start with a random ordering of the wizards.

The algorithm takes the wizard causing the most constraint violations and puts them in the place that causes the least amount of violations some of the time, and sometimes, based on chance, it moves a random wizard into his best spot.

If it goes too long without making progress, the entire list of wizards is shuffled.
