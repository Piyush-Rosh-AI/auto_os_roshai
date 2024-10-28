# auto_os_roshai
Make two terminal:
T1-for build and check with
git clone https://github.com/Piyush-Rosh-AI/auto_os_roshai.git src
sudo apt-get install libboost-all-dev


T2:opened dependencies folder to clone repo if required

git clone -b ros2 https://github.com/ros/bond_core.git
git clone https://github.com/BehaviorTree/BehaviorTree.CPP.git
git clone -b ros2 https://github.com/ros/diagnostic
sudo apt-get install xtensor-dev
git clone https://github.com/xtensor-stack/xsimd.git
git clone -b jazzy-devel https://github.com/cra-ros-pkg/robot_localization.git
git clone -b ros2 https://github.com/ros/xacro.git



Check for the following commands in case you witness some other dependencies issues--
    git clone -b ros2 https://github.com/ros-geographic-info/geographic_info.git
    sudo apt install ros-jazzy-test-msgs
    sudo apt-get install graphicsmagick libgraphicsmagick++-dev
    sud apt install libceres-dev
    git clone https://github.com/geographiclib/geographiclib.git
    sudo apt-get install libompl-dev ompl-demos
    sudo apt-get install libboost-filesystem-dev



