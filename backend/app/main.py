import os
if not file.filename.lower().endswith(".docx"):
raise HTTPException(status_code=400, detail="Please upload a .docx file")
if file.content_type not in (
"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
"application/octet-stream",
):
raise HTTPException(status_code=400, detail="Invalid content type for .docx")


content = await file.read()


# 1) extract plain text for placeholder detection
try:
# mammoth to HTML, then strip tags to text for robustness across runs
result = mammoth.convert_to_html(BytesIO(content))
html = result.value or ""
except Exception:
# fallback: python-docx paragraphs
doc = Document(BytesIO(content))
html = "\n".join(p.text for p in doc.paragraphs)


placeholders, matched_raw = extract_placeholders(html)


session_id = str(uuid.uuid4())
SESSIONS[session_id] = {
"filename": file.filename,
"doc_bytes": content,
"placeholders": placeholders,
"preview_html": naive_highlight(html, placeholders),
}


return ExtractResponse(
session_id=session_id,
filename=file.filename,
placeholders=placeholders,
chars=len(html),
)




@app.get("/session/{session_id}", response_model=SessionInfo)
async def get_session(session_id: str):
s = SESSIONS.get(session_id)
if not s:
raise HTTPException(status_code=404, detail="Session not found")
return SessionInfo(
session_id=session_id,
filename=s["filename"],
placeholders=s["placeholders"],
)




@app.post("/chat", response_model=ChatResponse)
async def chat_fill(req: ChatRequest):
s = SESSIONS.get(req.session_id)
if not s:
raise HTTPException(status_code=404, detail="Session not found")


ph: Placeholder | None = next((p for p in s["placeholders"] if p.id == req.placeholder_id), None)
if not ph:
raise HTTPException(status_code=404, detail="Placeholder not found")


# For assignment simplicity, we accept user's message as the final value.
# (Optionally call an LLM to validate/format; skipped to avoid key requirements.)
ph.value = req.message.strip()
ph.status = "filled"


reply = f"Recorded **{ph.display_name}** as: {ph.value}"
return ChatResponse(reply=reply, placeholder=ph)




@app.get("/download/{session_id}")
async def download_filled(session_id: str):
s = SESSIONS.get(session_id)
if not s:
raise HTTPException(status_code=404, detail="Session not found")
buf = fill_docx(s["doc_bytes"], s["placeholders"])
filename = s["filename"].rsplit(".docx", 1)[0] + "_filled.docx"
return StreamingResponse(BytesIO(buf), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={
"Content-Disposition": f"attachment; filename=\"{filename}\""
})
