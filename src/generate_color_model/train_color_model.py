import scipy.io as sio
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import os.path as osp
import cv2
import scipy.spatial.distance as ssd
import pickle
import scipy.cluster

def quantize(viz=False):
	dpath = '../data/IIIT5K'
	colors = np.zeros((5000, 4 * 3))  # (c1,c1_std,c2,c2_std) (foreground,background)
	i = 0
	for dset in ['test', 'train']:
		annfile = dset + 'CharBound'
		dat = sio.loadmat(dpath + '/' + annfile + '.mat')[annfile][0]
		N = dat.size
		# for j in xrange(N):
		for j in range(N):
			# print(i)
			imname = osp.join(dpath, dat[j]['ImgName'][0])
			im = scipy.ndimage.imread(imname)
			if im.ndim != 3:
				continue

			# make the image small if too big:
			is_big = np.array(im.shape[:2]) > 100
			if np.any(is_big):
				s = 100.0 / np.max(im.shape[:2])
				osize = s * np.array(im.shape)
				im = scipy.misc.imresize(im, osize.astype('int'))

			# convert to CIELAB color-space (useful for clustering):
			im2d_rgb = np.reshape(im, (np.prod(im.shape[:2]), 3)).astype(float)
			# im2d = cv.cvtColor(im, cv.cv.CV_RGB2Lab)
			im2d = cv2.cvtColor(im,cv2.COLOR_RGB2Lab)
			im2d = np.reshape(im2d, (np.prod(im.shape[:2]), 3)).astype(float)

			# cluster into 2 colors:
			# try:
			K = 3
			feat = scipy.cluster.vq.whiten(im2d)
			codes, _ = scipy.cluster.vq.kmeans(feat, K, iter=20, thresh=1e-05)
			labels, _ = scipy.cluster.vq.vq(feat, codes)

			# # keep the biggest two clusters :: << DOES NOT WORK
			# k_id = np.unique(labels)
			# k_num = np.array([np.sum(labels==k) for k in k_id])
			# k_id = np.argsort(-k_num)
			# print k_num, k_id

			# # Keep two clusters with largest distance and highest membership:
			# p = np.array([np.sum(labels==k)/len(labels) for k in np.unique(labels)])
			# p_mat = np.sqrt(np.outer(p,p))
			# #print p_mat
			dist_mat = ssd.squareform(ssd.pdist(codes))
			k_id = np.array(np.unravel_index(np.argmax(dist_mat), (K, K)))

			## need to regenerate the color (from original image)
			## this is because whitening makes us lose the color values:
			for k in range(2):
				codes[k, :] = np.mean(im2d[labels == k_id[k]], axis=0)

			# codes, labels = scipy.cluster.vq.kmeans2(imd2d, k=2, iter=20)
			# except:
			# 	continue
			# codes = codes[np.lexsort(codes.T),:]
			for k in range(2):
				# colors[i, k * 6:k * 6 + 3] = cv.cvtColor(codes[k, :][None, None, :].astype('uint8'), cv.cv.CV_Lab2RGB)
				colors[i, k * 6:k * 6 + 3] = cv2.cvtColor(codes[k, :][None, None, :].astype('uint8'), cv2.COLOR_Lab2RGB)
				colors[i, k * 6 + 3:k * 6 + 6] = np.std(im2d_rgb[labels == k], axis=0).astype('uint8')

			if viz:
				plt.clf()
				plt.subplot(1, 3, 1)
				plt.imshow(im)
				plt.subplot(1, 3, 2)
				plt.imshow((np.ones_like(im) * colors[i, 0:3][None, None, :]).astype('uint8'))
				plt.subplot(1, 3, 3)
				plt.imshow((np.ones_like(im) * colors[i, 6:9][None, None, :]).astype('uint8'))
				plt.show()
			i += 1

	colors = colors[:i, :]
	# save the color information:
	return colors


if __name__ == '__main__':
	color = quantize(False)
	with open('colors_new.cp', 'wb') as f:
		pickle.dump(color,f)