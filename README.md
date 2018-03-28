# Project Deduplication

Suppose two users uploads a same file on server,
files are same therefore to save two copies of same file 
is not a good idea,
on social sites also thousands of users uploads a same image,
video, mp3 files, on cloud.
and hence to use storage in more efficient way we have developed
"Reliability Aware Project Deduplication"

Data deduplication refers to a technique for eliminating
redundant data in a data set. In the process of deduplication,
extra copies of the same data are deleted, leaving only one copy
to be stored.

Data is analysed to identify duplicate byte patterns to ensure the
single instance of the duplicate part is considered and stored in
the server

There are two levels of deduplication
One is "File level deduplication", means that the whole file is compared to another
to detect duplication,
Example,
	comparing two books.

This method is enfficient,
Example,
	Ram and Shyam have the same copy of the book of 50 pages..
	Ram has deposited his book in the library(means uploaded his data)
	and Shyam cut 10 pages of the book and deposited it in the library.
	Now for the library, those are totally different books,
	library will store those 2 copies of books in the library..
	(Here library will store extra 40 pages..)
	
to avoid this situation there is second type of duplication,
"Block level deduplication"
	In this, we are making blocks/chunking/splitting files in a fixed size,
	and simply we are comparing them with existing blocks..
	like in above example..
	
	when ram submit his book in the library, the book will split with its pages
	and stored into the library...
	when Shyam submit his book in library, his book also will split in pages,
	and will get stored into library,
	Now library does not store extra 40 pages,
	it will just keep a record of permissions of users..
	like ram can access the whole book.
	and Shyam can access only 40 pages.

This whole idea is applied on files,
block size is 256KB
and to keep duplication count of blocks(pages) we have implemented a 
"In Memory Database"
(sorry for bad English!)
(To be continued..)
	


