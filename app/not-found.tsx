import Link from 'next/link';
export default function NotFound(){return <main className="standalone-state"><h1>Record or page not found</h1><p>This address does not match a page in the atlas.</p><Link className="outline-button" href="/rulers">Ruler explorer</Link><Link className="outline-button" href="/">Atlas overview</Link></main>}
