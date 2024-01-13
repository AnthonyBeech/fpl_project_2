# QC of Legacy Data

Unfortunately, it appears that the 2023-24 data is only partially correct. For example player Darren Randolph should have an id of 91 according to the fpl API. Hoever when we check the legacy data, we see the id is different. We can also confirm this by comparing the data from the API directly where we see that the fixture times do not match.

Therefore I will remove this daa from the extraction and replace it with the current API data, from which point I can auto populate as the weeks go on.

I will also make the bold assumption that previous years are also correct (this cannot be easily varified as the API does not store this legacy data)