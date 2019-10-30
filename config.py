class Config(object):
    DEBUG = True
    LOGGING_FILE_PATH = "/ece1779-manager-app.log"
    TESTING = False

    SECRET_KEY = "fe8e5c349e8eb13bf65bdc261229d43d"

    TARGET_GROUP_ARN = "arn:aws:elasticloadbalancing:us-east-1:935290738939:targetgroup/ECE1779A2-TG/91f7c395a87d8fac"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_DATABASE_URI = "mysql://ece1779a1:password123@localhost/ece1779a1"
    SQLALCHEMY_DATABASE_URI = "mysql://ece1779a2:password123@ece1779a2.csmeodxl9uyw.us-east-1.rds.amazonaws.com/ece1779a2"

    AMI_ID = 'ami-021060d50eca70067'
    INSTANCE_TYPE = 't2.small'
    KEYNAME = 'ECE1779A2'
    SG = ['sg-07d577ef4ae2d3dcb']
    ZONE = 'us-east-1a'
    EC2NAME = 'a2'
    SUBNETID = 'subnet-0669c0c16d554ce3f'

    MANAGER_NAME = 'ECE1779A2-manager-app'
    S3_BUCKET = "ece1779a2-rita"
