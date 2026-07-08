from django.shortcuts import render


def index(request, *args, **kwargs):
    """Serve the React SPA shell for every client-side route."""
    return render(request, "djangoapp/index.html")
