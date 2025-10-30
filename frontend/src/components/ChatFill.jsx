import React, { useMemo, useState } from 'react'
import { sendAnswer } from '../api'


export default function ChatFill({ sessionId, placeholders, onFilled }) {
const next = useMemo(()=> placeholders.find(p=>p.status==='pending'), [placeholders])
const [msg, setMsg] = useState('')
const [busy, setBusy] = useState(false)


if (!next) return <div className="card"><h3>3) All fields filled 🎉</h3><p>You can download your document now.</p></div>


const ask = `Enter ${next.display_name}`


const submit = async () => {
if (!msg.trim()) return
setBusy(true)
try {
const res = await sendAnswer(sessionId, next.id, msg.trim())
onFilled(res.placeholder)
setMsg('')
} catch (e) {
alert(e?.response?.data?.detail || 'Failed to record value')
} finally { setBusy(false) }
}


return (
<div className="card">
<h3>3) Fill fields (conversational)</h3>
<p><strong>Prompt:</strong> {ask}</p>
<input
placeholder={ask}
value={msg}
onChange={e=>setMsg(e.target.value)}
style={{width:'100%', padding:8, borderRadius:8, border:'1px solid #233345', background:'#0b0c10', color:'#eaf0f1'}}
/>
<div style={{marginTop:8}}>
<button onClick={submit} disabled={busy}>{busy? 'Saving...':'Save value'}</button>
</div>
<div style={{marginTop:12}}>
<small className="badge">Remaining: {placeholders.filter(p=>p.status==='pending').length}</small>
</div>
</div>
)
}
