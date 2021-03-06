# Note here, the metrics is only for the ELB not for every worker.
RequestCount_IN_REQUEST = {
      "view": "timeSeries",
      "width": 600,
      "height": 395,
      "metrics": [
          ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", "app/ECE1779A2-LB/9ca6ccb762876696", {"stat": "Sum"}]
      ],
      "period": 300,
      "start": "-PT1.5H",
      "stacked": False,
      "yAxis": {
          "left": {
              "min": 0,
          },
          "right": {
              "min": 0
          }
      }
    }
