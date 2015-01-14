# Strawberry_py

Strawberry_py is a tool made for simplifying the building and testing of iOS 
applications, written in python. 

It uses UIAutomation and aims to make it easy as pie, pun intended, to build
and run tests. The idea for this project was shamelessly based on bwoken.

### Why not just use bwoken?

* Bwoken requires a newer ruby version than the one that ships with OS X
* Bwoken requires too much fiddeling to get it to work (like Simulator version being mandatory etc)
* Bwoken requires quite a bit of ruby knowledge to tweak
* Bwoken is not very active
* Bwoken is really just made for testing

Don't get me wrong, I really like bwoken, but decided I wanted to create my own
alternative.

### Goals with Strawberry_py:

* Work out of the box on OS X
* Being small and to the point/easy to extend
* Being useful for building iOS applications, even when you don't want to do any 
testing

### Current status

Works:

* Building iOS project 
* Running the tests
* Generating commandline test reports
* Generating simple juint test reports
* Continue other tests after one fails
* Focus on a given set of tests
* Exclude a given set of tests

In progress:

* Generating alternative test reports
* Add ability to retry test
* Add ability to uninstall app between tests 

Doesn't work:

* Running the application (without testing)
* Generating build reports

