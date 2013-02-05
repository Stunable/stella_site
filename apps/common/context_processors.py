

def page_role(request):
    splits = request.path_info.split('/')
    print splits
    if not len(splits) > 2:
        return {'page_role':'shop'}
    if splits[1] == 'cart':
        return {'page_role':'cart'}
    
    return {'page_role': 'shop'}

   