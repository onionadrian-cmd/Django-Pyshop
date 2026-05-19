from .models import WebsiteCustomization


def customization_settings(request):
    customization = WebsiteCustomization.get_settings()
    return {'customization': customization}
