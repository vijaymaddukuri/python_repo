Prerequisistes :

1. You should have Python installed, if you don't then follow https://www.python.org/downloads/
2. You should have pip installed,if you don't then follow https://pip.pypa.io/en/stable/installing/
3. Port "5000" in your localhost is free.

===========================================================================================================

Steps to Run the API :

1. Unzip the folder Holoplot.zip 
2. Then run deploy.sh 
      
   This will install all the dependencies :
   1. Flask - The REST API Server
   2. Robot Framework - The Test Framework
   3. Requests - For Calling REST API
    
   
   And Start the Server :
   
   Go to the folder Holoplot/app/ and run :
   "python bing_bang_boom_server.py"
   This will run the server and make the API's for the game BingBangBoom available for the consumer/client.
   
   And you're All Set!!!
   
4. You can now access the API directly on your browser :
   HOMEPAGE : http://127.0.0.1:5000/api/v1/home [METHOD : GET]
   GET DOMAINS AND ROLES API :  http://127.0.0.1:5000/api/v1/domain/device_id [METHOD : GET]
    - Replace the device_id with the actual device id of the speaker.

===========================================================================================================	
Steps to run the Tests :

1. Ensure that the server in running[Step 3 in the section above].
2. Go to the folder Holoplot/tests/ and run :
   "robot bing_bang_boom_test.robot"
3. The tests will publish the report.html, log.html for the results and log respectively.

==============================================================================================================

   
   