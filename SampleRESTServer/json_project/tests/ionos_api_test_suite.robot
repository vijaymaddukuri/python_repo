*** Settings ***
Documentation   IONOS API Test Suite
...             This Test suite tests the IONOS API's ued for creation/updation/deletion of Datacenter , Servers ,
...             LANs, NICs.
Library         lib.workflow
Suite Teardown    Cleanup


*** Keywords ***
Cleanup
    # Deleting Datacenter
    delete data center     ${DATA_CENTER}

*** Test Cases ***
End to End IONOS Datacenter and Resource Provisioning using API
    # Create Data Center
    ${DATA_CENTER} =  create data center      create_datacenter.json     name=test data center    location=de/fra
    set global variable   ${DATA_CENTER}
    # Wait for the data center to get created
    sleep     15
    # Validate Data Center Is Available
    ${STATUS} =   validate data center is available     ${DATA_CENTER}
    should be equal as strings   ${STATUS}  True
    # Create a Private LAN
    ${PRIVATE_LAN} =  create lan    ${DATA_CENTER}     create_lan.json     name=test private lan     public=false
    # Create a Public LAN
    ${PUBLIC_LAN} =  create lan    ${DATA_CENTER}     create_lan.json       name=test public lan      public=true
    Sleep   30
    # Create a Server "Frontend"
    ${FRONTEND_SERVER} =  create server   ${DATA_CENTER}      create_server.json     name=test frontend server
    # Create a Server "Backend"
    ${BACKEND_SERVER} =  create server   ${DATA_CENTER}      create_server.json       name=test backend server
    sleep  20

    #  Create NIC's for the both the servers using Private LAN
    ${PrivateNIC_FRONTEND} =  create nic    ${DATA_CENTER}    ${FRONTEND_SERVER}   create_nic.json     name= nic private lan   lan=${PRIVATE_LAN}
    ${PrivateNIC_BACKEND} =  create nic    ${DATA_CENTER}    ${BACKEND_SERVER}   create_nic.json     name= nic private lan   lan=${PRIVATE_LAN}
    #  Create NIC for Frontend Server using Public LAN
    ${PublicNIC_FRONTEND} =  create nic    ${DATA_CENTER}    ${FRONTEND_SERVER}   create_nic.json     name= nic pubic lan   lan=${PUBLIC_LAN}
    #  Update Frontend Server's Configuration
    update server    ${DATA_CENTER}     ${FRONTEND_SERVER}    update_server.json   ram=2048    cores=2

    sleep    60

    # Validate Private  LAN is available
    ${STATUS} =   validate lan is available   ${DATA_CENTER}    ${PRIVATE_LAN}
    should be equal as strings    ${STATUS}   True
    # Validate Public LAN IS Available
    ${STATUS} =   validate lan is available   ${DATA_CENTER}    ${PUBLIC_LAN}
    should be equal as strings    ${STATUS}   True

    #Validate both Servers are connected to Private LAN through their respective NIC's
    ${STATUS} =  validate nic is available    ${DATA_CENTER}    ${FRONTEND_SERVER}    ${PrivateNIC_FRONTEND}
    should be equal as strings    ${STATUS}   True
    ${STATUS} =  validate nic is available    ${DATA_CENTER}    ${BACKEND_SERVER}    ${PrivateNIC_BACKEND}
    should be equal as strings    ${STATUS}   True

    #Validate the Public NIC is connected to Frontend Serverr
    ${STATUS} =  validate nic is available    ${DATA_CENTER}    ${FRONTEND_SERVER}    ${PublicNIC_FRONTEND}
    should be equal as strings    ${STATUS}   True

    #Validate FrontEnd Server is Running and validate the configuration
    ${STATUS} =  validate server configuration     ${DATA_CENTER}     ${FRONTEND_SERVER}    vmState=RUNNING    ram=2048   cores=2
    should be equal as strings   ${STATUS}    True
    #Validate Backend Server is Running and Validate the Configuration
    ${STATUS} =  validate server configuration     ${DATA_CENTER}      ${BACKEND_SERVER}    vmState=RUNNING    ram=1024   cores=1
    should be equal as strings   ${STATUS}    True














