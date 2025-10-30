import React, { useState } from 'react'
import { uploadDoc } from '../api'


export default function UploadBox({ onExtract }) {
const [file, setFile] = useState(null)
const [busy, setBusy] = useState(false)


const submit = async () => {
if (!file) return
setBusy(true)
try {
const res = await uploadDoc(file)
onExtract(res)
} catch (e) {
alert(e?.response?.data?.detail || 'Upload failed')
} finally { setBusy(false) }
}


return (
<div className="card">
<h3>1) Upload a .docx legal template</h3>
<input type="file" accept=".docx" onChange={e=>setFile(e.target.files?.[0]||null)} />
<button onClick={submit} disabled={!file || busy}>{busy?'Uploading...':'Extract placeholders'}</button>
<p className="badge">Supported patterns: {'{name}'}, {'{{name}}'}, {'[Company Name]'}, {'<Company Name>'}</p>
</div>
)
}
