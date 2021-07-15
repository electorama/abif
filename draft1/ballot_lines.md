## Ballot Lines

Lines of Ballot Data that are identical should be aggregated.

Lines of Ballot Data begin with the count of the ballot, followed by a colon. It is permitted to add space to Ballot Data to improve readability. Parsers ignore white space in data lines.

The Ballot Count is followed by the Ballot.

Optionally after the Ballot, additional extended data may be included. When the additional data is included a colon follows the ballots. The additional data is a JSON object enclosed in curly brackets {} and may not include any line-breaks, since they naturally terminate a line in ABIF. Adding Space is recommended for readability.

## Ballot Data

',' separates the values of a Cardinal Ballot or Weighted Ballot.

### Ordinal Ballots

Approval and Plurality Ballots use the Ordinal format.

'=' denotes that choices are ranked equally.

'>' denotes the choice to the left is preferred to the choice on the right.

### Cardinal Ballots

Commonly known as Score or Range Ballots.

'/' separates the choice identifier from the score.

### Weighted Ballots

For Cumulative Voting.

'\*' indicates that the choice before the '*' has been assigned the weight following it.

### Example Ballot Data
```
# Ordinal
1: A>B>C
# Ordinal with Equal Ranking
2: A>B=D>C
# Plurality
3: A
# Approval
4: A=C=X
# Cardinal
5: A/5,B/2,C/1,E/2
# Weighted
6: A*1,B*2,D*4

# Ranked with Extended Data
7: D>C>B>A: { "precinct":51, "county":"Bronx", "machine":"2" }
8: C>B>A: { "precinct":11, "county":"Queens", "machine":"Mail" }
```
### Comments

Issue #7 Separate standards for ranked vs. scored ballots
delimiter Issue #3
