#Install gcloud to system

curl https://sdk.cloud.google.com | bash
# exec -l $SHELL

export gcloud_path=/home/runner/google-cloud-sdk/
echo $gcloud_path

#install python and pip 0
sudo apt-get update -y
sudo apt-get -y install python2.7 python-pip


#installing requirements
pip --no-cache-dir install -r requirememts.txt

#run test 
python runner.py
