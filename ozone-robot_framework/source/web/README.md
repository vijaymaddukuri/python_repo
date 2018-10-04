# Ozone! The EMC EHC Manager

This project was developed as a proof-of-concept for EHC Build automation and configuration.

The solution is built on MEAN stack - 
 - [MongoDB](https://mongodb.com/)
 - [AngularJS](https://angulars.org/)
 - [AngularJS Material](https://material.angularjs.org/)
 - [Node.js and npm](nodejs.org) Node ^4.4.4, npm ^3.8.9
  
## Features
  - Import EHC Design
  - Create Projects to manage multiple EHC deployments
  - Automated Deploy of EHC components
  - Automated configuration
  - Monitoring and Managing

## Architecture
   
  - Web Server - MEAN Stack
  - Database - MongoDB
  - Queue Processor - Kue
  - Backend - Deployment and Automation - Ansible/Python
   
## Build and development

### Prerequisites

Install the below dependencies on a Linux Server - 64 bit.

1. First install GIT to download the source; Node for the web server and MongoDB for database. 
  - [Git](https://git-scm.com/)
  - [Node.js and npm](nodejs.org) Node ^4.2.3, npm ^2.14.7
  - [MongoDB](https://www.mongodb.org/) - Keep a running daemon with `mongod`

2. Use NPM to install bower and grunt-cli to build the application
  - [Bower](bower.io) (`npm install --global bower`)
  - [Grunt](http://gruntjs.com/) (`npm install --global grunt-cli`)

3. Install Python 3.4 and OVF_TOOL_4.1.0 for backend automation. This could be on the server as the web server or a different server. This is configured in the config file as 'scriptEngine'
  - [python 3.4](https://www.python.org/download/releases/3.4.0)
  - [OVF Tool 4.1.0](https://my.vmware.com/web/vmware/details?productId=491&downloadGroup=OVFTOOL410)

4. Download python scripts from a separate source

### Developing

1. Run `npm install` to install server dependencies.

2. Run `bower install` to install front-end dependencies.

3. Run `mongod` in a separate shell to keep an instance of the MongoDB Daemon running

4. Run `grunt serve` to start the development server. It should automatically open the client in your browser when ready.

## Update configuration options

Update file server/config/environment/production.js with necessary information such as:
1. Mongo DB URI - set to localhost if running MongoDB on same server
2. Set SMTP server information


## Build & development

Run `grunt build` for building and `grunt serve` for preview.

## Testing

Running `npm test` will run the unit tests with karma.

#Todo
- Automate further initial configuration of other items
- Testing - write test cases and test
- Improve code structure
- Documentation - API and Usage

#Author
Mumshad Mannambeth - <mumshad.mannambeth@emc.com>

This project was generated with the [Angular Full-Stack Generator](https://github.com/DaftMonk/generator-angular-fullstack) version 3.6.1.
