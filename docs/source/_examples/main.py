from pro_lambda import pro_lambda

some = pro_lambda(lambda : 1)
other = some + 1
# then we call result as if it was (lambda: 1)() + 1
assert other() == 2

some = pro_lambda(lambda x, y: x+y)
other = some + 1
# here we pass some arguments
assert other(1, 2) == 4

# we can also use another function on the right side
other = some + (lambda z, y: z - y)
assert other(1, y = 2, z = 3) == 4
