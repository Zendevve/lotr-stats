"use client";
export default function ErrorPage({reset}:{reset:()=>void}){return <main className="standalone-state" role="alert"><h1>This page could not load</h1><p>Retry the page. Downloaded data and saved queries are unaffected.</p><button className="primary-button" onClick={reset}>Retry</button><a className="outline-button" href="/">Atlas overview</a></main>}
