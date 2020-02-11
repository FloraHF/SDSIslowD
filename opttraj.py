from envelope import *
from overall_plot import triag_cnstr_3, triag_cnstr_2, triag_cnstr_1, plot_bds, plot_orbit




if __name__ == '__main__':

	r1, r2 = 6.1, 6.6 # dwin


	traj, ss, phis, rrs, ts = envelope_barrier(r1, r2)

	print(ss[105])


	N = 70
	dts = ts[N:105] - ts[N]
	print(dts)
	T = 1.1
	x1 = np.asarray(traj[N:105, 0])
	y1 = np.asarray(traj[N:105, 1])
	xi = np.asarray(traj[N:105, 2])
	yi = np.asarray(traj[N:105, 3])

	R = np.sqrt(xi[-1]**2 + yi[-1]**2)
	xt = np.array([R*cos(beta) for beta in np.linspace(0, 2*pi, 50)])
	yt = np.array([R*sin(beta) for beta in np.linspace(0, 2*pi, 50)])

	tht2 = atan2(yi[-2] - yi[-1], xi[-2] - xi[-1]) - acos(1/1.5)
	x2 = np.array([2+dts[-1] + T] + [2+dt for dt in dts[::-1]])*cos(tht2) + xi[-1]
	y2 = np.array([2+dts[-1] + T] + [2+dt for dt in dts[::-1]])*sin(tht2) + yi[-1]

	tht1 = atan2(y1[0] - y1[1], x1[0] - x1[1])
	x1 = np.concatenate((np.array([T*cos(tht1)+x1[0]]), x1))
	y1 = np.concatenate((np.array([T*sin(tht1)+y1[0]]), y1))

	thti = atan2(yi[0] - yi[1], xi[0] - xi[1])
	xi = np.concatenate((np.array([T*cos(thti)+xi[0]]), xi))
	yi = np.concatenate((np.array([T*sin(thti)+yi[0]]), yi))

	fig, ax = plt.subplots()
	ax.plot(x1, y1, 'b', alpha=0.8, marker='o', markevery=20, label='D')
	ax.plot(x2, y2, 'b', alpha=0.8, marker='o', markevery=20, label=None)
	ax.plot(xi, yi, color='xkcd:crimson', marker='o', markevery=20, alpha=0.8, label='I')
	for i, (x1_, y1_, x2_, y2_, xi_, yi_) in enumerate(zip(x1, y1, x2, y2, xi, yi)):
		if i%20 == 0:
			ax.plot([xi_, x1_], [yi_, y1_], 'k--')
			ax.plot([xi_, x2_], [yi_, y2_], 'k--')
		if i == len(xi)-1:
			ax.plot([xi_, x1_], [yi_, y1_], 'k--')
			ax.plot([xi_, x2_], [yi_, y2_], 'k--')
			ax.plot(x1_, y1_, 'o', color='b')
			ax.plot(x2_, y2_, 'o', color='b')
			ax.plot(xi_, yi_, 'o', color='xkcd:crimson')
	ax.plot(xt, yt, 'r', label='Target')

	plt.xlabel('x', fontsize=14)
	plt.ylabel('y', fontsize=14)
	ax.grid()
	ax.axis('equal')
	ax.legend(fontsize=14)
	plt.savefig('traj.png')
	plt.show()
