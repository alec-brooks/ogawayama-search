# Ogawayama Search

This is a scraper for the English language guide for Ogawayama, which is located at ogawayama.online

The intention is to make this online guide searchable and accessible

## Common Searches

As of the time of writing the data is only accessible in a newline delimited JSON format, for personal ease of querying.

At the moment it is recommended to query the data using the tool `jq` as such:

```bash
jq 'select(.quality > 2 and .grade == "5.7")' climbs.ndjson
```
