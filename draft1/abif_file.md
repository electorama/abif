## Aggregate Ballot Information (ABIF) File Format

Aggregate Ballot Information files end with the extension _.abif_ or _.ABIF_. ABIF files use the utf8 encoding.

A specific revision of utf8 may be set as a minimum by providing the optional metadata value utf8_revision.

Lines beginning with the '#' (Number Sign U+0023) character are comments and are ignored by parsers. Text enclosed in square brackets [] is quoted utf8 text, to avoid confusion it may not contain the [] bracket characters themselves.

No escaping mechanism is defined and comments beginning later in a line are unsupported.

Lines end with the New Line (Line Feed U+000A) \\n character.

Comments and text in square brackets may be any valid utf8 characters that have a visible representation or are part of a combining sequence that produces one. White space characters except New Line and the standard space character should not be used, and should be ignored (stripped) by parsers. Control Characters, Unassigned Code Points and any others that produce no visible representation should not be present in ABIF files.

ABIF is designed to permit human editing, the tools used my leave Byte Order Markers and unwanted space characters such as Line Feed \\r. Parsers for ABIF should therefore discard these characters. It is left to the parser to decide whether to ignore Control Characters and Unassigned Code Points or to consider them fatal.

The metadata and ballot data sections of an ABIF file should only contain the characters [a-zA-Z0-9\\n _] and punctuation characters such as ':' that have defined functions within ABIF. The full utf8 character set is only permitted within comments and brackets [].

ABIF files are organized with the metadata first followed by the ballot lines. It is recommended to keep comments with the metadata, but they may appear anywhere in the file.

# Comments

square brackets #5
the meta data dictionary #14 has not defined utf versioning or character set information yet and the metadata format #6 is still open.
