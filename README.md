# autonomous_car

Start

  |
  V

  Initialize Camera
  Set Camera Parameters
  Initialize shared variable (prox)

  |
  V

  Start 'read_distance' Process (Background)
  Set Process as Daemon
  Main Loop

  |
  V

  Capture Frame from Camera

  |
  V

  Detect Traffic Light (Red/Green/Unknown)

  |
  V

  Read Proximity Sensor (Background Process)

  |
  V

  Process Camera Image for Lane Detection

  |
  V

  - Apply Image Processing (Color Filters, Edge Detection)
  - Detect Lane Lines
  - Calculate Lane Center

  |
  V

  Check for Obstacles and Traffic Light

  |
  V

  - If Obstacle Detected within 25cm:
    - Stop the Car
  - If Red Traffic Light Detected:
    - Stop the Car
  - If Lane Center Shifted Left:
    - Turn Left
  - If Lane Center Shifted Right:
    - Turn Right
  - Otherwise:
    - Continue Forward

  |
  V

  Display Camera Feed with Lane and Traffic Light Indicators

  |
  V

  Check for User Quit (Press 'q' Key)

  |
  V

End