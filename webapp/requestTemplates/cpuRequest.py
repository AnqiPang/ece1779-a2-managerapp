CPUUtilization_REQUEST = {
      "view": "timeSeries",
      "width": 600,
      "height": 395,
      "metrics": [
          ["AWS/EC2", "CPUUtilization", "InstanceId", "value of instance id", {"stat": "Sum"}]
      ],
      "period": 60,
      "start": "-PT0.5H",
      "stacked": False,
      "yAxis": {
          "left": {
              "min": 0.1,
          },
          "right": {
              "min": 0
          }
      }
    }
