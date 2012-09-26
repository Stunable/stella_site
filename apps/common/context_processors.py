
"""
def SEO(request):
    splits = request.path_info.split('/')
    deep_roles = {
        'projects'  :   {
             2 : 'list'
            ,3 : 'detail'
            ,4 : 'item_detail'
            ,5 : 'item_detail'
            ,6 : 'media_detail'
        },
        '':{
            0 : 'home',
            1 : 'home',
            2 : 'home'

        }
    }
    try:
        out = [splits[1]]+[deep_roles[splits[1]][len(splits)]]
    except:
        return {'page_role': request.path_info.replace('/','_').lstrip('_').rstrip('_')}

    return {'page_role':'_'.join(out)}
"""