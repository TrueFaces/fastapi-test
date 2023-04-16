from fastapi import Request

def get_domain(request:Request):
    return request.url.scheme + "://" + request.url.hostname