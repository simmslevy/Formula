from Events import *

"""
                         2012 Endurance

2012_endurance.add_feature(Straight(length=63.3))
2012_endurance.add_feature(Straight(length=5.3))
2012_endurance.add_feature(Straight(length=3.53))
2012_endurance.add_feature(Straight(length=3.97))
2012_endurance.add_feature(Straight(length=5.74))
2012_endurance.add_feature(Straight(length=19.43))
2012_endurance.add_feature(Straight(length=38.42))
2012_endurance.add_feature(Straight(length=7.73))
2012_endurance.add_feature(Straight(length=7.73))
2012_endurance.add_feature(Straight(length=8.59))
2012_endurance.add_feature(Straight(length=11.16))
2012_endurance.add_feature(Straight(length=49.23))
2012_endurance.add_feature(Straight(length=63.87))
2012_endurance.add_feature(Straight(length=5.32))
2012_endurance.add_feature(Straight(length=4))
2012_endurance.add_feature(Straight(length=5.32))
2012_endurance.add_feature(Straight(length=5.32))
2012_endurance.add_feature(Straight(length=7.32))
2012_endurance.add_feature(Straight(length=10.65))
2012_endurance.add_feature(Straight(length=10.65))
2012_endurance.add_feature(Straight(length=11.43))
2012_endurance.add_feature(Straight(length=11.43))
2012_endurance.add_feature(Straight(length=49.23))
2012_endurance.add_feature(Straight(length=68.57))
2012_endurance.add_feature(Straight(length=6.15))
2012_endurance.add_feature(Straight(length=17.58))
2012_endurance.add_feature(Straight(length=8.79))
2012_endurance.add_feature(Straight(length=7.03))

2012_endurance.add_feature(Corner(radius=17.66, length=))
2012_endurance.add_feature(Corner(radius=8.83, length=))
2012_endurance.add_feature(Corner(radius=18.55, length=))
2012_endurance.add_feature(Corner(radius=8.83, length=))
2012_endurance.add_feature(Corner(radius=23.84, length=))
2012_endurance.add_feature(Corner(radius=31.79, length=))
2012_endurance.add_feature(Corner(radius=18.89, length=))
2012_endurance.add_feature(Corner(radius=12.02, length=))
2012_endurance.add_feature(Corner(radius=18.89, length=))
2012_endurance.add_feature(Corner(radius=14.6, length=))
2012_endurance.add_feature(Corner(radius=53.24, length=))
2012_endurance.add_feature(Corner(radius=19.2, 14.17, 8.79, length=))
2012_endurance.add_feature(Corner(radius=15.23, 14.57, length=))
2012_endurance.add_feature(Corner(radius=6.62, length=))
2012_endurance.add_feature(Corner(radius=13.9, length=))
2012_endurance.add_feature(Corner(radius=10.6, length=))
2012_endurance.add_feature(Corner(radius=16.55, length=))
2012_endurance.add_feature(Corner(radius=13.87, length=))
2012_endurance.add_feature(Corner(radius=18.29, length=))
2012_endurance.add_feature(Corner(radius=26.975, length=))
2012_endurance.add_feature(Corner(radius=19.81, length=))
2012_endurance.add_feature(Corner(radius=14.07, length=))
2012_endurance.add_feature(Corner(radius=10.97, 9.144, length=))
2012_endurance.add_feature(Corner(radius=8.38, 8.38, length=))
2012_endurance.add_feature(Corner(radius=12.65, length=))
2012_endurance.add_feature(Corner(radius=17.68, length=))
2012_endurance.add_feature(Corner(radius=10.36, 9.144, length=))
2012_endurance.add_feature(Corner(radius=11.58, length=))

                         self._num_laps = 19
                         self._num_straights = 28
                         self._dist_straights = [63.3, 5.3, 3.53, 3.97, 5.74, 19.43, 38.42, 7.73, 7.73, 8.59, 11.16, 49.23, 63.87, 5.32, 4, 5.32, 5.32, 7.32, 10.65, 10.65, 11.43, 11.43, 49.23, 68.57, 6.15, 17.58, 8.79, 7.03]
                         self._num_corners = [1,1,1,1,1,1,1,1,1,1,1,3,2,1,1,1,1,1,1,1,1,1,2,2,1,1,2,1]
  [17.66],[8.83],[18.55],[8.83],[23.84],[31.79],[18.89], [12.02], [18.89], [14.6], [53.24], [19.2, 14.17, 8.79], [15.23, 14.57], [6.62], [13.9], [10.6], [16.55], [13.87], [18.29], [26.975], [19.81], [14.07], [10.97, 9.144], [8.38, 8.38], [12.65], [17.68], [10.36, 9.144], [11.58]]
                         self._corner_dist = [[18.03], [6.63], [7.12], [7.86], [5.83], [43.56], [4.29], [7.34], [7.58], [10.45],
                                              [4.65], [21.78, 29.92, 25], [11.7, 16.27], [5.2], [8.98], [6.47], [10.69], [31.47],
                                              [19.15], [67.8], [40.11], [22.59], [11.68, 11.65], [7.75, 14.77], [18.99], [71.59],
                                              [19.71, 12.77], [36.38]]


                         2014 Endurance

2014_endurance.add_feature(Straight(length=80.28))
2014_endurance.add_feature(Straight(length=37.22))
2014_endurance.add_feature(Straight(length=8.42))
2014_endurance.add_feature(Straight(length=65.09))
2014_endurance.add_feature(Straight(length=21.88))
2014_endurance.add_feature(Straight(length=14.73))
2014_endurance.add_feature(Straight(length=20.75))
2014_endurance.add_feature(Straight(length=13.94))
2014_endurance.add_feature(Straight(length=60.13))
2014_endurance.add_feature(Straight(length=8.72))
2014_endurance.add_feature(Straight(length=10.29))
2014_endurance.add_feature(Straight(length=8.16))
2014_endurance.add_feature(Straight(length=46.50))
2014_endurance.add_feature(Straight(length=60.46))
2014_endurance.add_feature(Straight(length=21.62))
2014_endurance.add_feature(Straight(length=47.74))
2014_endurance.add_feature(Straight(length=18.35))
2014_endurance.add_feature(Straight(length=27.64))

2014_endurance.add_feature(Corner(radius=27.07, 10.03, 14.26, 7.50, 11.11, 43.78, length=))
2014_endurance.add_feature(Corner(radius=11.04, length=))
2014_endurance.add_feature(Corner(radius=19.74, length=))
2014_endurance.add_feature(Corner(radius=10.70, 33.82, 35.87, length=))
2014_endurance.add_feature(Corner(radius=23.48, 30.0, length=))
2014_endurance.add_feature(Corner(radius=14.15, 18.04, 22.05, 20.30, 18.72, length=))
2014_endurance.add_feature(Corner(radius=27.78, length=))
2014_endurance.add_feature(Corner(radius=24.23, length=))
2014_endurance.add_feature(Corner(radius=17.65, length=))
2014_endurance.add_feature(Corner(radius=20.35, length=))
2014_endurance.add_feature(Corner(radius=17.60, 38.13, 20.80, length=))
2014_endurance.add_feature(Corner(radius=49.70, length=))
2014_endurance.add_feature(Corner(radius=18.47, 25.07, length=))
2014_endurance.add_feature(Corner(radius=11.60, length=))
2014_endurance.add_feature(Corner(radius=28.11, length=))
2014_endurance.add_feature(Corner(radius=110.37, 18.56, length=))
2014_endurance.add_feature(Corner(radius=13.99, 9.81, length=))
2014_endurance.add_feature(Corner(radius=28.79, 16.75, length=))

                         self._num_straights = 18
80.28, 37.22, 8.42, 65.09, 21.88, 14.73, 20.75, 13.94, 60.13, 8.72, 10.29, 8.16, 46.50, 60.46, 21.62, 47.74, 18.35, 27.64
                         self._num_corners = [6,1,1,3,2,5,1,1,1,1,3,1,2,1,1,2,2,2]
                         self._radii = [[16.35, 13.79, 16.35, 16.24, 16.19, 19.16], [9.32], [7.51], [14.90, 17.80, 17.71], [9.93, 10.04],
                                        [13.78, 13.30, 12.65, 14.88, 17.74], [26.35], [10.62], [16.86], [14.53], [21.28, 41.27, 20.47],
                                        [19.22], [10.20, 9.03], [19], [13.90], [26.07, 12.82], [16.05, 18.79], [9.23, 11.66]]
                         self._corner_dist = [27.07, 10.03, 14.26, 7.50, 11.11, 43.78], [11.04], [19.74], [10.70, 33.82, 35.87], [23.48, 30.0], [14.15, 18.04, 22.05, 20.30, 18.72], [27.78], [24.23], [17.65], [20.35], [17.60, 38.13, 20.80], [49.70], [18.47, 25.07], [11.60], [28.11], [110.37, 18.56], [13.99, 9.81], [28.79, 16.75]


                                              [23.98], [17.27], [10.59, 10.83, 9.52], []]
"""
