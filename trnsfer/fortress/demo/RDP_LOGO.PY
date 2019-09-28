import rdp

'''
tolerance = 70
min_angle = np.pi*0.22
filename = os.path.expanduser('~/tmp/bla.data')
points = np.genfromtxt(filename).T
print(len(points))
x, y = points.T

simplified = np.array(rdp.rdp(points.tolist(), tolerance))

print(len(simplified))
'''
print(rdp.rdp([[1,1],[2,1],[3,1],[4,1],[4,2],[4,3],[4,4]]))


