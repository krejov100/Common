import pyrealsense2 as rs

def post_process(image):
	spatial_filter = rs.spatial_filter()
	temporal_filter = rs.temporal_filter()
	hole_filling_filter = rs.hole_filling_filter()

	filter_magnitude = rs.option.filter_magnitude
	filter_smooth_alpha = rs.option.filter_smooth_alpha
	filter_smooth_delta = rs.option.filter_smooth_delta

	spatial_filter.set_option(filter_magnitude, 2)
	spatial_filter.set_option(filter_smooth_alpha, 0.5)
	spatial_filter.set_option(filter_smooth_delta, 20)
	temporal_filter.set_option(filter_smooth_alpha, 0.4)
	temporal_filter.set_option(filter_smooth_delta, 20)

	# Apply the filters
	filtered_frame = spatial_filter.process(image)
	filtered_frame = temporal_filter.process(filtered_frame)
	#filtered_frame = hole_filling_filter.process(filtered_frame)

	return filtered_frame

