# IN424


## Create a ROSject
Connect to [RDS](https://app.theconstructsim.com/#/) with your user and password.

Go to "My rosjects" and run the project that you created.



## Clone the Project repository
In the same terminal, follow the instructions **ONE AFTER THE OTHER**:

```bash
cd ~/catkin_ws/src && git clone https://github.com/JohvanyROB/IN424.git

cd ~/catkin_ws && catkin_make --pkg in424_msgs && source ~/catkin_ws/devel/setup.bash

catkin_make && source ~/catkin_ws/devel/setup.bash
```

You can now come back to the project subject. 
