import math
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
from helper import *

class PointSet:
	def __init__(self, num_red_pts, num_blue_pts):
		self.red_points = []
		self.blue_points = []
		self.extra_red = False
		self.extra_blue = False 
		self.min_interval_size = 1

		self.generate_point_set(int(num_red_pts), int(num_blue_pts))
		
		self.point_set = self.red_points + self.blue_points
		if(int(num_red_pts)%2 == 0):
			self.extra_red = self.red_points.pop()
		if(int(num_blue_pts)%2 == 0):
			self.extra_blue = self.blue_points.pop()

		#extra red and blue  points are not included in this set
		self.red_duals = [dual_line(point) for point in self.red_points]
		self.blue_duals = [dual_line(point) for point in self.blue_points]

	def generate_point_set(self, num_red_pts, num_blue_pts):
		self.red_points = random_point_generator(num_red_pts)
		self.blue_points = random_point_generator(num_blue_pts)
		self.print_point_set()

	def print_point_set(self):
		print("\n---Red points---\n")
		for i in range(len(self.red_points)):
			print(self.red_points[i])
		print("\n---Blue points---\n")
		for i in range(len(self.blue_points)):
			print(self.blue_points[i])	
		#plot_points(self)
	
	def find_xcoord_bound(self):
		min_x = min(self.point_set, key=lambda P: P.x).x
		max_x = max(self.point_set, key=lambda P: P.x).x
		return min_x, max_x

	def find_ycoord_bound(self):
		min_y = min(self.point_set, key=lambda P: P.y).y
		max_y = max(self.point_set, key=lambda P: P.y).y
		return min_y, max_y

	def find_median_level(self, x, lines):
		y_vals = [line.b + (x * line.m) for line in lines]
		y_vals.sort()
		med = math.floor((len(y_vals) + 1) / 2)
		return y_vals[med-1]

	def get_intersections(self, duals):
		intersections = []
		duals = self.red_duals + self.blue_duals
		for i in range(len(duals)):
			for j in range(len(duals)):
				if (i < j):
					intersection_ = get_intersection(duals[i], duals[j])       
					if intersection_.x == np.inf:
						pass
					elif self.interval[0] < intersection_.x and self.interval[1] > intersection_.x:
						intersections.append(intersection_)
					else:
						pass

		intersections.sort(key = lambda I: I.x)
		return intersections

	def get_med_linestring(self, duals, intersections, color):
		med_levels = [Point(self.interval[0], self.find_median_level(self.interval[0], duals))]
		med_levels.extend([Point(inter.x, self.find_median_level(inter.x, duals)) for inter in intersections])
		med_levels.extend([Point(self.interval[1], self.find_median_level(self.interval[1], duals))])

		for i in range(0,len(med_levels)-1):
			x1, x2 = med_levels[i].x, med_levels[i+1].x
			y1, y2 = med_levels[i].y, med_levels[i+1].y
			plt.plot([x1, x2], [y1, y2], linestyle='-', color = color, linewidth=3)
			plt.pause(0.5)

		return LineString(med_levels)
    
	def median_intersection(self, time_pause=1):
		red_intersections = self.get_intersections(self.red_duals)
		blue_intersections = self.get_intersections(self.blue_duals)

		min_y, max_y = self.find_ycoord_bound()
		prepare_axis(self.interval[0]-1, self.interval[1]+1, min_y-5,max_y+5)

		plt.title('Median Levels')
		red_med_linestring = self.get_med_linestring(self.red_duals, red_intersections, color='red')
		blue_med_linestring = self.get_med_linestring(self.blue_duals, blue_intersections, color='blue')

		ham_cut_points = red_med_linestring.intersection(blue_med_linestring)
		if isinstance(ham_cut_points, Point):
			ham_cut_points = [ham_cut_points]
		ham_cut_dual = [dual_line(point) for point in ham_cut_points]

		for point in ham_cut_points:
			plot_point(point, marker='*', color = 'purple', size=20)

		input('Ready to check out the Ham Sandwich Cut? :D')
		plt.gca().clear()
		plt.title('Ham Sandwich Cut')
		min_x, max_x = self.find_xcoord_bound()
		prepare_axis(min_x-5, max_x+5, min_y-5, max_y+5)

		for point in ham_cut_points:
			plot_point(point, marker= '*', color='black', size=20)

		plot_points(self)
		for hc in ham_cut_dual:
			plot_line(hc, color='orange')
		plt.pause(1)
		input('Wanna leave?')

	def display_interval_medlevel_intersection(self, interval):
		left_red_med = self.find_median_level(interval[0], self.red_duals)
		left_blue_med = self.find_median_level(interval[0], self.blue_duals)

		right_red_med = self.find_median_level(interval[1], self.red_duals)
		right_blue_med = self.find_median_level(interval[1], self.blue_duals)

		# interval_medians = [Point(interval.l, l_red_med), Point(interval.l, l_blue_med), Point(interval.r, r_red_med), Point(interval.r, r_blue_med)]
		med_intersections = [left_red_med, left_blue_med, right_red_med, right_blue_med]
		min_y, max_y = min(med_intersections),  max(med_intersections)
		prepare_axis(interval[0]-5, interval[1]+5, min_y-5,max_y+5)
		self.intervalymin = min_y
		self.intervalymax = max_y

	    # plot_interval
		plt.axvline(x=interval[0], linestyle='--', color='yellow')
		plt.axvline(x=interval[1], linestyle='--', color='yellow')
		plt.pause(0.5)
	        
		plot_point(Point(interval[0], left_red_med), color='red', marker='*',size=15)
		plot_point(Point(interval[0], left_blue_med), color='blue', marker='*', size=15)
		plot_point(Point(interval[1], right_red_med), color='red', marker='*', size=15)
		plot_point(Point(interval[1], right_blue_med), color='blue', marker='*', size=15)

	def odd_intersection(self, interval):
		l = interval[0]
		r = interval[1]

		lmr = self.find_median_level(l, self.red_duals)
		lmb = self.find_median_level(l, self.blue_duals)

		rmr = self.find_median_level(r, self.red_duals)
		rmb = self.find_median_level(r, self.blue_duals)

		return (lmr - lmb)*(rmr - rmb) < 0

	def find_cut(self, time_pause=0.8):
		plt.gca().clear()
		min_x, max_x = self.find_xcoord_bound()
		min_y, max_y = self.find_ycoord_bound()
		self.interval = [min_x-40, max_x+40]

		prepare_axis(self.interval[0]-5, self.interval[1]+5, min_y-5, max_y+5)
		plt.title('Points')
		plot_points(self)

		plt.gca().clear()
		prepare_axis(self.interval[0]-5, self.interval[1]+5, min_y-5, max_y+5)
		plt.title('Points and Duals')
		plot_points_and_duals(self)
		
		plt.title('Binary Search')
		self.display_interval_medlevel_intersection(self.interval)
		
		while (self.interval[1]-self.interval[0]) > self.min_interval_size:
		    mid = float((self.interval[0] + self.interval[1]) / 2.0)
		    left_int = [self.interval[0], mid]
		    right_int = [mid, self.interval[1]]

		    self.display_interval_medlevel_intersection(left_int)
		    #input("checking left half of the interval")
		    plt.pause(time_pause)
		    self.display_interval_medlevel_intersection(right_int)
		    #input("checking right half of the interval")
		    plt.pause(time_pause)

		    if self.odd_intersection(left_int):
		        self.interval = left_int
		    else:
		        self.interval = right_int

		   
		    self.display_interval_medlevel_intersection(self.interval)

		plt.pause(time_pause)
		self.median_intersection()

num_red_pts = input("Enter the number of desired red points\n")
num_blue_pts = input("Enter the number of desired blue points\n")
points = PointSet(num_red_pts, num_blue_pts)
points.find_cut()