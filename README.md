# bikeshed-data

The [Bikeshed](https://github.com/tabatkins/bikeshed) document processor
relies on information from several external services
for several of its features —
autolinking, bibliographies, etc.

This project fetches all the information Bikeshed needs
and digests it directly into the format Bikeshed wants to work with,
so that Bikeshed's update process can run as quickly and smoothly as possible,
while also limiting the stress on the databases that source the data.

You probably don't want to file a bug on this project;
most likely, you want to file it on [Bikeshed](https://github.com/tabatkins/bikeshed/issues/).
However, if this project stops updating for some reason
(it typically recieves a new commit at least twice an hour),
feel free to file an issue,
as the updater process may have fallen over
and be in need of manual restarting.

## My Spec Is Missing From Bikeshed?

Bikeshed draws most of its data from [Browser Specs](https://github.com/w3c/browser-specs),
which should capture all the specs (W3C and otherwise)
that are relevant for web browsers.
If your spec isn't on [the list](https://github.com/speced/bikeshed-data/blob/main/data/specs.json) but you think it fits that bill,
[file an issue on Browser Specs](https://github.com/w3c/browser-specs/issues/new).

## Running Manually

Normally this project is updated automatically several times a day.
However, if the update process falls over,
it can be run manually.
To do so, install [Bikeshed](https://github.com/tabatkins/bikeshed) normally,
then clone this repository
and run `python __init__.py` in the folder.

This will invoke `git` on your system,
so it'll only work if you have commit rights to this project;
contact me if it's necessary for me to grant that to you.
