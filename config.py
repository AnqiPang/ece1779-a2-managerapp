class Config(object):
    DEBUG = True
    LOGGING_FILE_PATH = "/ece1779-manager-app.log"
    TESTING = False

    SECRET_KEY = "fe8e5c349e8eb13bf65bdc261229d43d"

    TARGET_GROUP_ARN = "arn:aws:elasticloadbalancing:us-east-1:935290738939:targetgroup/ECE1779A2-TG/91f7c395a87d8fac"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql://ece1779a2:password123@ece1779a2.csmeodxl9uyw.us-east-1.rds.amazonaws.com/ece1779a2"

