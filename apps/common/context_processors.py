

def page_role(request):
    splits = request.path_info.split('/')
    print splits
    if not len(splits) > 2:

        return {'page_role':'shop'}
    
    return {'page_role': 'shop'}

   