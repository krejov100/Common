import pyrealsense as rs
from PostProcess import post_process

class RosBagGenerator:
	def __init__(self, ros_file_path, max_distance):
		self.max_distance = max_distance
		config = rs.config()
		config.enable_device_from_file(ros_file_path)
		self.pipeline = rs.pipeline()
		self.profile = self.pipeline.start(config)
		self.depths = []

		frame_number = 0
		while True:
			frames = self.pipeline.wait_for_frames()
			if frames[0].get_frame_number() < frame_number:
				break
			frame_number = frames[0].get_frame_number()
			if frames:
				self.intrin = frames.get_profile().as_video_stream_profile().get_intrinsics()
				depth = frames.get_depth_frame()
				self.depths.append(depth)

	def grab(self):
		for depth in (self.depths):
			depth = post_process(depth)
			depth_data = depth.as_frame().get_data()
			depth_image = np.asanyarray(depth_data)
			depth_scale = self.profile.get_device().first_depth_sensor().get_depth_scale()
			max_value = self.max_distance / depth_scale
			depth_image[depth_image > max_value] = max_value

			yield depth_image, self.intrin


