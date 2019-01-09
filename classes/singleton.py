class _TestA(object):
	def __init__(self):
		print 'creating instance of Test_A'


class _TestB(object):
	def __init__(self):
		print 'creating instance of Test_B'


def create_singleton(cls):
	instances = {}

	def get_instance(*args, **kwargs):
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)

		return instances[cls]

	return get_instance


TestA = create_singleton(_TestA)
TestB = create_singleton(_TestB)

test_a = TestA()
test_b = TestB()
