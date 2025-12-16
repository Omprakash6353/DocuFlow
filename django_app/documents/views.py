# django_app/documents/views.py
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse

from .models import Document, AuditLog

# Simple debug printer (server console)
def dbg(msg, *args):
    try:
        print("[DBG]", msg % args if args else msg)
    except Exception:
        print("[DBG]", msg, args)


@csrf_protect
def custom_login(request):
    dbg("custom_login called; method=%s", request.method)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        dbg("POST login username=%s password=%s", username, "<hidden>")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            dbg("login success for %s", username)
            return redirect("dashboard")
        else:
            dbg("login failed for %s", username)
            return render(request, "login.html", {"error": "Invalid username or password"})
    # GET
    get_token(request)
    return render(request, "login.html")


def custom_logout(request):
    dbg("custom_logout called for user=%s", getattr(request.user, "username", None))
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    """
    Dashboard view — compute metrics in view and pass to template.
    Template won't call .filter() or .count() itself.
    """
    dbg("dashboard called for user=%s", request.user.username)

    my_documents = Document.objects.filter(created_by=request.user).order_by("-id")
    my_tasks = Document.objects.filter(approver=request.user, status="submitted").order_by("-id")

    # Simple metrics (counts)
    total_documents = my_documents.count()
    submitted_count = my_documents.filter(status="submitted").count()
    approved_count = my_documents.filter(status="approved").count()
    rejected_count = my_documents.filter(status="rejected").count()

    return render(request, "documents/dashboard.html", {
        "my_documents": my_documents,
        "my_tasks": my_tasks,
        "metrics": {
            "total": total_documents,
            "submitted": submitted_count,
            "approved": approved_count,
            "rejected": rejected_count,
        }
    })


@login_required
def create_document(request):
    dbg("create_document called; method=%s user=%s", request.method, request.user.username)
    if request.method == "POST":
        title = request.POST.get("title") or ""
        description = request.POST.get("description") or ""
        file = request.FILES.get("file")
        approver_id = request.POST.get("approver")

        approver = User.objects.get(id=approver_id) if approver_id else None

        document = Document.objects.create(
            title=title.strip(),
            description=description.strip(),
            file=file,
            created_by=request.user,
            approver=approver,
            status="draft"
        )

        if request.POST.get("action") == "submit":
            document.status = "submitted"
            document.save()
            AuditLog.objects.create(document=document, user=request.user, action="submitted", comment="Submitted for approval")

        return redirect("dashboard")

    users = User.objects.exclude(id=request.user.id)
    return render(request, "documents/create_document.html", {"users": users})


@csrf_protect
@login_required
def document_detail(request, document_id):
    """
    Fixed document_detail — always returns an HttpResponse and handles GET/POST cleanly.
    """
    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        return HttpResponse("Document not found", status=404)

    logs = document.audit_logs.all().order_by("-timestamp")

    if request.method == "POST":
        action = request.POST.get("action")
        comment = request.POST.get("comment", "")

        # Submit (creator only)
        if action == "submit" and request.user == document.created_by:
            document.status = "submitted"
            document.save()
            AuditLog.objects.create(document=document, user=request.user, action="submitted", comment="Submitted for approval")
            return redirect("document_detail", document_id=document.id)

        # Approve (approver only)
        if action == "approve" and request.user == document.approver:
            # try calling FastAPI (best-effort)
            try:
                if settings.FASTAPI_URL:
                    requests.post(
                        f"{settings.FASTAPI_URL.rstrip('/')}/workflow/action/",
                        json={
                            "document_id": document.id,
                            "action": "approve",
                            "actor": request.user.id,
                            "comment": comment,
                        },
                        headers={"api_token": settings.API_TOKEN},
                        timeout=5
                    )
            except Exception as e:
                dbg("FastAPI error: %s", e)

            document.status = "approved"
            document.save()
            AuditLog.objects.create(document=document, user=request.user, action="approved", comment=comment)
            return redirect("document_detail", document_id=document.id)

        # Reject (approver only)
        if action == "reject" and request.user == document.approver:
            document.status = "rejected"
            document.save()
            AuditLog.objects.create(document=document, user=request.user, action="rejected", comment=comment)
            return redirect("document_detail", document_id=document.id)

        # Fallback: go back to same page
        return redirect("document_detail", document_id=document.id)

    # GET - render page
    return render(request, "documents/document_detail.html", {
        "document": document,
        "logs": logs,
    })