def obj_to_post(obj):
    post = dict(vars(obj))

    # convert to string

    if obj.category:
        post['category'] = obj.category.name
    else:
        post['category'] = 'NoCategory'
    
    # = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    if obj.image:
        post['image'] = obj.image.url
    else:
        post['image'] = 'https://via.placeholder.com/900x300/'

    if obj.modify_dt:
        post['modify_dt'] = obj.modify_dt.strftime('%B %d, %Y')
    else:
        post['modify_dt'] = ''
    
    if obj.tags:
        post['tags'] = [tag.name for tag in obj.tags.all()]
    else:
        post['tags'] = []
    
    if obj.owner:
        post['owner'] = obj.owner.username
    else:
        post['owner'] = 'Anonymous'

    del post['_state'], post['category_id'], post['create_dt']

    return post

def prev_next_post(obj):
    try:
        prevObj = obj.get_prev()
        prevDict = {
            'id': prevObj.id,
            'title': prevObj.title,
        }
    except obj.DoesNotExist:
        prevDict = {}
    
    try:
        nextObj = obj.get_next()
        nextDict = {
            'id': nextObj.id,
            'title': nextObj.title,
        }
    except obj.DoesNotExist:
        nextDict = {}

    return prevDict, nextDict