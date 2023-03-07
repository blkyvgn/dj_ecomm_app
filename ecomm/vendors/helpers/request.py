
def get_arguments_dict():
	return {'full_name':set(), 'attributes':set(), 'price_min':None, 'price_max':None}

def get_filter_arguments(request):
	arguments = get_arguments_dict()
	if request.GET:
		for key, val in request.GET.lists():
			if key == 'full_name':
				arguments['full_name'] = arguments['full_name'].union(set(val))
			elif key == 'price_min':
				arguments['price_min'] = val.pop()
			elif key == 'price_max':
				arguments['price_max'] = val.pop()
			else:
				arguments['attributes'] = arguments['attributes'].union(set(val))
		setattr(request, 'filter_arguments', arguments)
	else:
		if hasattr(request, 'filter_arguments'):
			arguments = request.filter_arguments
	return arguments