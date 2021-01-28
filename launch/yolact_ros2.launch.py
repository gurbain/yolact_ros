from ament_index_python.packages import get_package_share_directory
import os

from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch import LaunchDescription

params_file = 'yolact_config.yaml'

def generate_launch_description():

    # Load params
    pkg_dir = get_package_share_directory('yolact_ros2')
    config_file = os.path.join(pkg_dir, 'config', params_file)

    # Rectify image
    # image_processing_node_container = ComposableNodeContainer(
    #     name='image_proc_container',
    #     package='rclcpp_components',
    #     executable='component_container',
    #     namespace='image_proc',
    #     composable_node_descriptions=[
    #         ComposableNode(
    #             package='image_proc',
    #             plugin='image_proc::RectifyNode',
    #             name='rectify_node',
    #             # Remap subscribers and publishers
    #             remappings=[
    #                 # Subscriber remap
    #                 ('image', '/t265/fisheye1/image_raw_rt'),
    #                 ('camera_info', '/t265/fisheye1/camera_info_rt'),
    #                 ('image_rect', 'image_rect')
    #             ],
    #         )],
    #     output='screen'
    # )
    image_processing_node = Node(
        package='treebot_processing',
        executable='t265_rectifier',
        name='t265_rectifier',
        output='screen',
    )

    # Detect
    yolact_ros_node = Node(
        package='yolact_ros2',
        executable='yolact_ros2_node',
        name='yolact_ros2_node',
        output='screen',
        parameters=[config_file]
    )

    ld = LaunchDescription()
    ld.add_action(image_processing_node)
    ld.add_action(yolact_ros_node)

    return ld
