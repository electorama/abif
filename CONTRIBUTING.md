Please contribute!  There is still a lot of work that needs to happen to make the ABIF specification ready to submit to an organization that deals with technical specifications.  A list of items that need to be done can be found here:
* FIXME-link-to-bug-tracker

It was only in 2025 that Lark-based parser became useful for converting ABIF into "jabmod" (the JSON ABif MODel).  It's not perfect, but it may one day replace the regex-based monstrosity that powers [abiftool](https://electorama.com/abiftool) and [awt](https://electorama.com/awt).  See [issue FIXME in the abiftool bug tracker](FIXME) to learn more about that.

The "election-software" mailing list is a good place to stay up-to-date on the latest news associated with ABIF:
* https://electorama.com/es

If you contribute, please make sure you agree to the licence (both [for the software](https://www.apache.org/licenses/LICENSE-2.0.html) and [for the specification](https://creativecommons.org/licenses/by-sa/4.0/)).  Links to both can be found here:
* https://github.com/electorama/abif/blob/main/LICENSE

### Policy Changelog
Below is a reverse-chronological log of changes to the ABIF contribution policy.

#### 2025-06-12

Added many links above.

#### 2022-01-23

Per [the January 2022 newsletter](https://github.com/electorama/abif/discussions/28), here's the licenses you need to agree to in order to do much of anything with the bits found in this repository:

* The [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.html) for software.
* The [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) for the specification.

One thing I'll add: we also need to consider the [IETF's RFC 8179](https://datatracker.ietf.org/doc/html/rfc8179).  Do not try to interject stealth patents into this specification.

Please agree to the license for this repository before contributing:
* https://github.com/electorama/abif/blob/main/LICENSE

#### 2021-06-13

We need to solve a few things before accepting serious contributions:

* Copyright: what license will the reference implementation be under?  Probably MIT, but there's at least a couple of scenarios where [@robla](https://github.com/robla) could imagine Apache of even AGPL to be more appropriate.
* Copyright assignment: do we need this?
* Patent policy: do we need to make sure we aren't subject to stealth patenting of our work here?
