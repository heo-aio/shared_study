export default function Layout({ children }) {

    return (
        <html lang={"ko"}>
            <head>
                <meta charSet={"utf-8"}/>
                <title>client 와 server 연동</title>
            </head>
            <body>
                {children}
            </body>
        </html>
    );
}