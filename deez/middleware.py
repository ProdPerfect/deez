class Middleware:
    def __init__(self, resource):
        self.resource = resource

    def before_request(self, request):
        pass

    def before_response(self, response):
        pass


class WildCardDomainResolverMiddleware(Middleware):
    def before_request(self, request):
        domain_name = request.lambda_context.get('domainName')
        domain_prefix = request.lambda_context.get('domainPrefix')
        request.request_domain_name = domain_name
        request.request_domain_prefix = domain_prefix
        return request
