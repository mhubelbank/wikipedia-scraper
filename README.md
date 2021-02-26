## README
#### Authored by user @mhubelbank.

This small repo contains an interactive Python web-scraping script and sample output txt. The script reads from the [Long Wiki pages list](https://en.wikipedia.org/w/index.php?title=Special:LongPages) using the BeautifulSoup library, randomly selects pages from the list, and parses through HTML to obtain a specified number of variable-length outputs from each page. There is programmatic filtration of certain terms and articles based on trends observed via testing, as well as regex auto-formatting. Finally, the user must approve or deny each selected text via console interaction; there is a max number of selection attempts for each source, and we pull from a given source at most one time.
