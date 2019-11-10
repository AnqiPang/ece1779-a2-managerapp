Requests_bulabula = {
    "view": "timeSeries",
    "width": 600,
    "height": 395,
    "stacked": False,
    "metrics": [
        [ "RequestsEC2", "Counting", "Instance", "ValueOfInstanceID",{ "stat": "Sum", "period": 60 } ]
    ],
    "region": "us-east-1",
    "start": "-PT1.5H",
    "yAxis": {
        "left": {
            "min": 0,
        },
        "right": {
            "min": 0
        }
    }
}