import h5py
import cv2
import os
import numpy as np

def save_image_h5(input_path, output_path, filename):
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	image_h5 = h5py.File(output_path + os.sep + filename, 'w')
	for f in os.listdir(input_path):
		file_path = os.path.join(input_path, f)
		image = cv2.imread(file_path)
		image = image[:, :, ::-1]
		img_shape = image.shape
		image_h5.create_dataset(f, (img_shape[2], img_shape[1], img_shape[0]), dtype='u8',data=image.T)


def getFileNameAndExt(path):
	(filepath, tempfilename) = os.path.split(path)
	(shortname, extension) = os.path.splitext(tempfilename)
	return shortname, extension


def merge_h5(input_path, output_path,filename):
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	dset_file = h5py.File(output_path + os.sep + filename, 'w')
	for root, dirs, files in os.walk(input_path):
		for f in files:
			file_path = os.path.join(root, f)
			# print file_path
			if getFileNameAndExt(file_path)[0] == 'depth':
				depth = h5py.File(file_path, 'r')
				dset_depth = dset_file.create_group('depth')
				for f in depth.keys():
					depth_data = np.zeros((2,depth[f].shape[0],depth[f].shape[1]),'float32')
					depth_data[0,:,:] = depth[f][:]
					depth_data[1, :, :] = depth[f][:]
					dset_depth.create_dataset(f, (2,depth[f].shape[0],depth[f].shape[1]), dtype='float32',data=depth_data)
			elif getFileNameAndExt(file_path)[0] == 'image':
				image = h5py.File(file_path, 'r')
				dset_image = dset_file.create_group('image')
				for f1 in image.keys():
					dset_image.create_dataset(f1, (image[f1].shape[2], image[f1].shape[1], image[f1].shape[0]), dtype='uint8',data=image[f1][:].T)
				# print image[f1][:]
			elif getFileNameAndExt(file_path)[0] == 'seg_uint16':
				seg = h5py.File(file_path, 'r')
				dset_seg = dset_file.create_group('seg')
				# print seg['mask'].keys()
				for f2 in seg['mask'].keys():
					# print seg['mask'][f2]
					dts = dset_seg.create_dataset(f2, (seg['mask'][f2].shape[0], seg['mask'][f2].shape[1]), dtype='uint16',data=seg['mask'][f2][:])
					dts.attrs['area'] = seg['mask'][f2].attrs['area']
					dts.attrs['label'] = seg['mask'][f2].attrs['label']
			else:
				continue


if __name__ == '__main__':
	# input_path = r'E:\opensource_project\SynthText-master\prep_scripts\image'
	# output_path = r'E:\opensource_project\SynthText-master\prep_scripts\h5'
	# save_image_h5(input_path,output_path,'image.h5')
	input_path = r'E:\opensource_project\SynthText-master\prep_scripts\h5'
	output_path = r'E:\opensource_project\SynthText-master\prep_scripts\h5'
	merge_h5(input_path, output_path,'dset.h5')
