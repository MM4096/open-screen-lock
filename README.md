# Open Screen Lock

A Screen Time application for Linux systems

## Features

- Set time limits for individual applications
- Increase or decrease existing time limits
- Forces apps to close after the limit is reached

### How does it work?
`OpenScreenLock` is made of two components:
- `OpenScreenLock` - the main application
- `OpenScreenLock-Background` - the background process that monitors the time and notifies the user

The config files store the time limits for each application, as well as elapsed time.
Normal users only have read access, and root permissions are needed to write to said files.

The background program must be run with root permissions, and it ticks up a timer each second. 

## Installation
1. Download the latest release from the [release page](https://github.com/mm4096/open-screen-lock/releases)
    1. You DO NOT need to download all the files. `OpenScreenLock`, `OpenScreenLock-Background` are required components,
       but `OpenScreenLock-TimeNotifier` is optional (enables notifications).
2. Make the files executable: `chmod +x OpenScreenLock OpenScreenLock-Background`
3. The first time you run the application and when you want to change the time limits, run `OpenScreenLock` with `root`
   permissions.