from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from .models import ChatSession, Message, UserProfile
from .services.llm_service import LLMService
import json

llm_service = LLMService()

@login_required
def chat_view(request):
    """Render the main chat interface."""
    chat_sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chat/chat.html', {'chat_sessions': chat_sessions})

@login_required
@require_http_methods(["POST"])
def create_chat_session(request):
    """Create a new chat session."""
    chat_session = ChatSession.objects.create(
        user=request.user,
        title=request.POST.get('title', 'New Chat')
    )
    return JsonResponse({
        'id': chat_session.id,
        'title': chat_session.title,
        'created_at': chat_session.created_at.isoformat()
    })

@login_required
@require_http_methods(["POST"])
def send_message(request, session_id):
    """Send a message and get a response from the LLM."""
    try:
        chat_session = ChatSession.objects.get(id=session_id, user=request.user)
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Create user message
        Message.objects.create(
            chat_session=chat_session,
            role='user',
            content=user_message,
            tokens_used=llm_service.count_tokens(user_message)
        )

        # Check cache for similar messages
        cache_key = f"chat_response_{hash(user_message)}"
        cached_response = cache.get(cache_key)
        
        if cached_response:
            response_data = cached_response
        else:
            # Generate response from LLM
            response_data = llm_service.generate_response(user_message)
            cache.set(cache_key, response_data, timeout=3600)  # Cache for 1 hour

        # Create assistant message
        Message.objects.create(
            chat_session=chat_session,
            role='assistant',
            content=response_data['response'],
            tokens_used=response_data['tokens_used'],
            model_used=response_data['model']
        )

        # Update user profile statistics
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.total_tokens_used += response_data['tokens_used']
        user_profile.save()

        return JsonResponse(response_data)

    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Chat session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_chat_history(request, session_id):
    """Get the chat history for a specific session."""
    try:
        chat_session = ChatSession.objects.get(id=session_id, user=request.user)
        messages = Message.objects.filter(chat_session=chat_session)
        
        return JsonResponse({
            'messages': list(messages.values('role', 'content', 'created_at', 'tokens_used', 'model_used'))
        })
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Chat session not found'}, status=404)

@login_required
def get_user_stats(request):
    """Get user statistics."""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        return JsonResponse({
            'total_tokens_used': user_profile.total_tokens_used,
            'total_chat_sessions': user_profile.total_chat_sessions,
            'preferred_model': user_profile.preferred_model
        })
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404) 