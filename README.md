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
