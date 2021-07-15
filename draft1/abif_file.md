# Aggregate Ballot Information (ABIF) File Format

Aggregate Ballot Information files end with the extension _.abif_ or _.ABIF_. ABIF files use the utf8 encoding.

Lines beginning with the '#' (Number Sign U+0023) character are comments and are ignored by parsers. Text enclosed in square brackets [] is quoted utf8 text, to avoid confusion it may not contain the [] bracket characters themselves.

No escaping mechanism is defined and comments beginning later in a line are unsupported.

Lines end with the New Line (Line Feed U+000A) \\n character.

Comments and text in square brackets may be any valid utf8 characters that have a visible representation or are part of a combining sequence that produces one. White space characters except New Line and the standard space character should not be used, and should be ignored (stripped) by parsers. Control Characters, Unassigned Code Points and any others that produce no visible representation should not be present in ABIF files.

ABIF is designed to permit human editing, the tools used my leave Byte Order Markers and unwanted space characters such as Carriage Return \\r. parsers for ABIF should discard these characters.

The metadata and ballot data sections of an ABIF file should only contain the characters [a-zA-Z0-9_], Space, New Line and punctuation characters such as ':' that have defined functions within ABIF. The full utf8 character set is permitted within comments, brackets [], and for values within encapsulated JSON.

ABIF files are organized with the metadata first followed by the ballot lines. It is recommended to keep comments with the metadata, but they may appear anywhere in the file.

## Header

An ABIF file which contains only Ballot Lines is not required to include the header. The Header is a single line beginning with ABIF, followed optionally by a version number. After the version number serialized data may be embedded (see the Meta Data section)

```
  ABIF
  ABIF 1.0
  ABIF 1.0 { ... }
```

### Comments on this draft section

square brackets #5

the meta data dictionary #14 has not defined utf versioning or character set/ culture information yet and the metadata format #6 is still open.
