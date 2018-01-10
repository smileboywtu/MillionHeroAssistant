from . import get
from . import process


def search(keyword, **kwargs):
    kwargs.setdefault('convey', False)
    page = get.page(keyword)
    results = process.page(page)
    if kwargs['convey']:
        for result in results:
            result.convey_url()
    return results
