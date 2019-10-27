CPUUtilization_REQUEST = {
      "width": 600,
      "height": 395,
      "metrics": [
          ["AWS/EC2", "CPUUtilization", "InstanceId", "value of instance id", {"stat": "Average"}]
      ],
      "period": 300,
      "stacked": False,
      "yAxis": {
          "left": {
              "min": 0.1,
              "max": 1
          },
          "right": {
              "min": 0
          }
      }
    }
