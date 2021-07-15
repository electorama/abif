# Meta Data

ABIF may optionally contain additional data either about the election or about Ballot Lines.

## Embedded Serialized Data

Serialized Data may be embedded as a JSON object. The JSON block may contain no line breaks. Where this is permitted it must be after any other data on that line.

## Meta Data in Header

A Serialized (JSON) block containing metadata values may be placed at the end of the ABIF Header Line. If this form is used, all Meta Data should be within the block. For longer Meta Data the Lines format should be used instead.

## Meta Data Lines

Between the Header and the beginning of Ballots, Meta Data items may appear one per line as key value pairs separated by a colon. Keys and Bare values may not contain spaces and are restricted to limited characters (defined in the File Format section). Brackets [] are used to delimit unicode string values. MetaData keys may contain numbers but must begin with a word character.

## Lists in Meta Data

List Items begin with an equal sign '=', followed by the identifier (key), then a colon followed by the bracketed descriptive text associated with that key.

The Default list is the *@choices* available in the election. Another common list is *@divisions*. To set the list for which subsequent choice list lines will be assigned, the list directive is the at sign '@' followed by the list name. Each List Item will be processed as part of the last list directive seen, if no list directive then *@choices*.

```
  @choices
  =TARG:[Daenerys Targaryen]
  =STRK:[Sansa Stark]
  =LANN:[Cersei Lannister]
  @divisions
  ="NWF2":[Northern Kingdom, Winterfell Precinct 2, Winterfell Town]
```

## Extended Ballot Data

For additional data, a final colon may be added followed by an embedded Serialized String (JSON).

```JSON
  11:STARK>TARGARYEN>LANNISTER:{"division": "FLEABOTTOM4", "city": "King's Landing" }
```
