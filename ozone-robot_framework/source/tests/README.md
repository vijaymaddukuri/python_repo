Web testing with Robot Framework and Selenium2Library
=====================================================

[Robot Framework](http://robotframework.org/) is a generic open source test automation framework and Selenium2Library Robot Framework is one of the many test libraries that can be used with it. In addition to showing how they can be used together for web testing, this demo introduces the basic Robot Framework test data syntax, how tests are executed, and how logs and reports look like.

Test cases
----------

Test case files as well as a resource file used by them are located in the respective directories.

**valid\_login.robot**  
A test suite with a single test for valid login.

This test has a workflow that is created using keywords in the imported resource file.

**invalid\_login.robot**  
A test suite containing tests related to invalid login.

**resource.robot**  
A resource file with reusable keywords and variables.

The system specific keywords created here form our own domain specific language. They utilize keywords provided by the imported [Selenium2Library][Robot Framework].

See [Robot Framework User Guide](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html) for more details about the test data syntax.

Generated results
-----------------

After running tests Robot Framework you will get report and log in HTML format.

Enable this to view Robot results from Jenkins
    
Jenkins -->  Manage Jenkins -->  Script Console
    
    System.setProperty("hudson.model.DirectoryBrowserSupport.CSP","sandbox allow-scripts; default-src 'none'; img-src 'self' data: ; style-src 'self' 'unsafe-inline' data: ; script-src 'self' 'unsafe-inline' 'unsafe-eval' ;")

Also set jenkins time zone if required
    
    System.setProperty('org.apache.commons.jelly.tags.fmt.timeZone', 'America/New_York')

Running demo
------------

### Preconditions

A precondition for running the tests is having Robot Framework and Selenium2Library Robot Framework installed, and they in turn require Python Robot Framework. Robot Framework [installation instructions] cover both Robot and Python installations, and Selenium2Library has its own installation instructions.

In practice it is easiest to install Robot Framework and Selenium2Library along with its dependencies using [pip][Robot Framework] package manager. Once you have pip installed, all you need to do is running these commands:

    pip install robotframework
    pip install robotframework-selenium2library

Download Chrome driver from here

https://chromedriver.storage.googleapis.com/2.27/chromedriver_linux64.zip

Commands  on OpenSuse
    
    # Install chrome
    zypper install chromium
    
    # Install Chrome driver for OpenSuse
    wget https://chromedriver.storage.googleapis.com/2.27/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    
    # Move to usr bin so it can be executed by robot framework
    mv chromedriver /usr/bin/
    
    # Install chromedriver dependency if required
    zypper install GConf2
    
    # Install Xcfb for headless testing
    zypper install -y xorg-x11-server
    
    # Install pip modules for AngularJS and xvfb for headless testing
    pip install robotframework-angularjs
    pip install robotframework-xvfb
    
    # Install SSHLibrary
    pip install robotframework-sshlibrary
    
### Running tests

The test cases Robot Framework are located in the `login_tests` directory. They can be executed using the `robot` command:

    robot browser/valid_login.robot

If you are using Robot Framework 2.9 or earlier, you need to  
use the `pybot` command instead.

You can also run an individual test case file and use various command line options supported by Robot Framework:

    robot browser/valid_login.robot
    robot --test InvalidUserName --loglevel DEBUG login_tests

Run `robot --help` for more information about the command line usage and see [Robot Framework User Guide][Robot Framework] for more details about test execution in general.

Using different browsers —–

  [installation instructions](https://github.com/robotframework/robotframework/blob/master/INSTALL.rst)
  
  [Selenium Library](https://github.com/robotframework/Selenium2Library/blob/master/INSTALL.rst)