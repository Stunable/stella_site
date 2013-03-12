

def page_role(request):
    splits = request.path_info.split('/')
    # print splits
    
    if request.subdomain == 'stylists':
        if splits[1] in ['accounts', 'registration']:
             pass
        else:
    	    return {'page_role':'retailers'}
    

    if not len(splits) > 2:
        return {'page_role':'shop'}



    
    

   
    return {'page_role':splits[1],'page_sub_role':splits[2]}
    
    # return {'page_role': 'shop'}

   
