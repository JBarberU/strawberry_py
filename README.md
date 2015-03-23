# Strawberry_py

Strawberry_py is a tool made for simplifying the building and testing of iOS
applications, written in python.

It uses UIAutomation and aims to make it easy as pie, pun intended, to build
and run tests. The idea for this project was shamelessly based on bwoken.

### Installation

* Make sure you have python 2.7 installed (which you should as it's bundled with
  OS X)
* Make sure your CLI has access to your certificates (through Keychain)
* Install your provisioning profiles in
  `"$HOME/Library/MobileDevice/Provisioning Profiles"` (by copying them there)
* Copy `straw_conf.sample.json` and change the config to suit your needs
* Export an xcode workspace (File->Save As Workspace...)

### Trouble shooting

* See Installation, in particular the code signing and workspace stuff

### Why not just use bwoken?

* Bwoken requires a newer ruby version than the one that ships with OS X
* Bwoken requires too much fiddeling to get it to work (like Simulator version
  being mandatory etc)
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


