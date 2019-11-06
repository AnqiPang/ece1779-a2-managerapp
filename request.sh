#!/bin/bash
before=$(wc -l < /home/ubuntu/Desktop/ece1779-userapp/access.log)
sleep 60
after=$(wc -l < /home/ubuntu/Desktop/ece1779-userapp/access.log)
#let dif=after-before
Requests=$($after-$before)
InstanceID=$(GET http://169.254.169.254/latest/meta-data/instance-id)

aws cloudwatch put-metric-data --metric-name Counting --dimensions Instance=$instanceID  --namespace "RequestsEC2" --unit Count --value $Requests
#aws cloudwatch put-metric-data --metric-name IO_WAIT --dimensions Instance=i-0c51f9f1213e63159  --namespace "Custom" --value $IO_WAIT
#/home/ubuntu/Desktop/ece1779-userapp/access.log# #