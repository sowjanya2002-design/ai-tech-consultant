"""Describe a screenshot with Claude so its content becomes searchable."""
import base64, os
import anthropic, httpx

def describe_image(url: str) -> str:
    data = httpx.get(url, timeout=30).content
    media = "image/png" if url.lower().endswith(".png") else "image/jpeg"
    msg = anthropic.Anthropic().messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5"), max_tokens=400,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media, "data": base64.b64encode(data).decode()}},
            {"type": "text", "text": "Describe this help-center screenshot: menus, buttons, settings and values shown."}]}])
    return msg.content[0].text
