import random
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, LineString

def random_point_generator(n, lower_bound=-10, upper_bound=10):
	points = []
	for i in range(n):
		x = random.uniform(lower_bound, upper_bound)
		y = random.uniform(lower_bound,upper_bound)
		points.append(Point(x, y))
	return points

def dual_line(point):
	return Line(point.x, -point.y)

def get_intersection(l1, l2):
	x = np.inf
	y = np.inf

	if l1.m != l2.m:
		x = (l2.b - l1.b) / (l1.m - l2.m)
		y = l1.m * x + l1.b
	return Point(x, y)

def prepare_axis(min_x=-10,max_x=10,min_y=-10,max_y=10):
	plt.grid(False,which='major')
	ax = plt.gca()
	ax.set_xlim(min_x,max_x)
	ax.set_ylim(min_y,max_y)
	plt.xticks(np.arange(min(np.array(ax.get_xlim())), max(np.array(ax.get_xlim()))+1, 1.0))
	plt.yticks(np.arange(min(np.array(ax.get_ylim())), max(np.array(ax.get_ylim()))+1, 1.0))
	plt.axhline(0, color='green')
	plt.axvline(0, color='green')

def plot_line(line, color):
	axes = plt.gca()
	x_vals = np.array(axes.get_xlim())
	y_vals = line.b + line.m * x_vals
	plt.plot(x_vals, y_vals, ls='--', color=color)

def plot_point(point, color, marker='o', size=5):
	plt.plot(point.x, point.y, color=color, marker=marker, markersize=size)

def plot_points(obj, time_pause=0.1):
	for i in range(len(obj.red_points)):		
		plot_point(obj.red_points[i], color='red')
		plt.draw()
		plt.pause(time_pause)
	
	if obj.extra_red:
		plot_point(obj.extra_red, color='red')
		plt.pause(time_pause)

	for i in range(len(obj.blue_points)):		
		plot_point(obj.blue_points[i], color='blue')
		plt.draw()
		plt.pause(time_pause)	
	
	if obj.extra_blue:
		plot_point(obj.extra_blue, color='blue')
		plt.pause(time_pause)	

def plot_points_and_duals(obj, time_pause=0.1):
	for i in range(len(obj.red_points)):		
		plot_point(obj.red_points[i], color='red')
		plt.draw()
		plt.pause(time_pause)
		plot_line(obj.red_duals[i], color='red')
		plt.pause(time_pause)

	if obj.extra_red:
		plot_point(obj.extra_red, color='red')
		plt.pause(time_pause)
		plot_line(dual_line(obj.extra_red), color='red')
		plt.pause(time_pause)

	for i in range(len(obj.blue_points)):		
		plot_point(obj.blue_points[i], color='blue')
		plt.draw()
		plt.pause(time_pause)
		plot_line(obj.blue_duals[i], color = 'blue')
		plt.pause(time_pause)

	if obj.extra_blue:
		plot_point(obj.extra_blue, color='blue')
		plt.pause(time_pause)
		plot_line(dual_line(obj.extra_blue), color='blue')
		plt.pause(time_pause)
	#plt.show()

class Line:
	def __init__(self, m, b):
		self. m = m
		self.b =  b