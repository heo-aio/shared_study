export default function Layout({ children }) {

    return(
        <html lang={'ko'}>
            <head>
                <meta charSet="utf-8" />
                <title>JEST</title>
            </head>
            <body>{children}</body>
        </html>
    );
}