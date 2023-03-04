from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods

from martor.utils import LazyEncoder

def obj_to_post(obj):
    post = dict(vars(obj))
    #post = model_to_dict(obj)

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

def make_tag_cloud(qsTag):
    minCount = min(tag.count for tag in qsTag)
    maxCount = max(tag.count for tag in qsTag)

    # minWeight, maxWeight = 1, 3
    def get_weight_func(minWeight, maxWeight):
        if minCount == maxCount:
            factor = 1.0
        else:
            factor = (maxWeight - minWeight) / (maxCount - minCount)

        def func(count):
            weight = round(minWeight + (factor * (count - minCount)))
            return weight

        return func

    weight_func = get_weight_func(1, 3)
    tagList = []
    for tag in qsTag:
        weight = weight_func(tag.count)
        tagList.append({
            'name': tag.name,
            'count': tag.count,
            'weight': weight,
        })

    return tagList

# @staff_member_required
@require_http_methods(["POST"])
def markdown_uploader(request):
    """
    Markdown image upload for locale storage
    and represent as json to markdown editor.

    Taken from https://github.com/agusmakmun/django-markdown-editor/wiki
    """
    if 'markdown-image-upload' in request.FILES:
        image = request.FILES['markdown-image-upload']
        image_types = [
            'image/png', 'image/jpg',
            'image/jpeg', 'image/pjpeg', 'image/gif'
        ]
        if image.content_type not in image_types:
            return JsonResponse(
                {
                    'status': 405,
                    'error': _('Bad image format.')
                }, encoder=LazyEncoder, status=405)

        if image.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            to_MB = settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024)
            return JsonResponse(
                {
                    'status': 405,
                    'error': _('Maximum image file is %(size)s MB.') % {'size': to_MB}
                }, encoder=LazyEncoder, status=405)

        img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
        tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
        def_path = default_storage.save(tmp_file, ContentFile(image.read()))
        img_url = os.path.join(settings.MEDIA_URL, def_path)

        return JsonResponse({
            'status': 200,
            'link': img_url,
            'name': image.name
        })
    return HttpResponse(_('Invalid request!'))