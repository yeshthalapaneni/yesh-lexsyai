import React, { useState } from 'react'
import UploadBox from './components/UploadBox'
import ChatFill from './components/ChatFill'
import Preview from './components/Preview'


export default function App() {
const [session, setSession] = useState(null)


const onExtract = (res) => {
setSession({
session_id: res.session_id,
filename: res.filename,
placeholders: res.placeholders
})
}


const onFilled = (updated) => {
setSession(s => ({
...s,
placeholders: s.placeholders.map(p=> p.id===updated.id? updated: p)
}))
}


return (
<div className="container">
<h1>Lexsy DocFiller</h1>
<p>Upload a legal template (.docx), fill placeholders conversationally, and download the completed document.</p>


<div className="row">
<div>
<UploadBox onExtract={onExtract} />
{session && <ChatFill sessionId={session.session_id} placeholders={session.placeholders} onFilled={onFilled} />}
</div>
<div>
{session && <Preview sessionId={session.session_id} filename={session.filename} placeholders={session.placeholders} />}
</div>
</div>


<footer style={{marginTop:24, opacity:.8}}>
<small>For Lexsy assignment • Demo use only • No data persisted</small>
</footer>
</div>
)
}
