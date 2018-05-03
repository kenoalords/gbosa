from utils.ip import get_tags

def tags_context_processor(request):
    return { 'tags': get_tags() }
