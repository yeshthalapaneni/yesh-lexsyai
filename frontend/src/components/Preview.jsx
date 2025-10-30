import React from 'react'
import { downloadUrl } from '../api'


export default function Preview({ sessionId, filename, placeholders }) {
const filled = placeholders.filter(p=>p.status==='filled').length
const total = placeholders.length


return (
<div className="card">
<h3>4) Preview & Download</h3>
<p><strong>File:</strong> {filename} &nbsp; <span className="badge">{filled}/{total} filled</span></p>
<div style={{display:'flex', gap:12, flexWrap:'wrap'}}>
<a href={downloadUrl(sessionId)}><button disabled={total>0 && filled<total}>Download DOCX</button></a>
{total>0 && filled<total && <span className="badge">Fill all fields to enable download</span>}
</div>
</div>
)
}
