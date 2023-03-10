def get_prev_next(instance):
    try:
        prev = instance.get_prev()
    except instance.DoesNotExist:
        prev = None
    
    try:
        next_ = instance.get_next()
    except instance.DoesNotExist:
        next_ = None
    
    return prev, next_

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