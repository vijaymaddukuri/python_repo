##################################################################################################################################
# EHC 4.1.1 Autodeploy docker image
#
##################################################################################################################################

The docker image produced by the Bamboo build is directly pushed to the dockerhub at emccorp/ozone registry.
If you have a dockerhub login and you have read permission to access emccorp/ozone registry, you can login into dockerhub and do a pull of the docker image with the below command.

docker pull emccorp/ozone:build-<xxx>.
Substitute <xxx> with the build number.