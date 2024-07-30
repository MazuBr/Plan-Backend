from fastapi.responses import HTMLResponse
from fastapi import APIRouter


graphql_router = APIRouter()

@graphql_router.get("/graphiql", tags=['graphql'])
async def graphiql():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GraphiQL</title>
        <link href="https://unpkg.com/graphiql/graphiql.min.css" rel="stylesheet" />
    </head>
    <body style="margin: 0; overflow: hidden;">
        <div id="graphiql" style="height: 100vh;"></div>
        <script crossorigin src="https://unpkg.com/react/umd/react.production.min.js"></script>
        <script crossorigin src="https://unpkg.com/react-dom/umd/react-dom.production.min.js"></script>
        <script crossorigin src="https://unpkg.com/graphiql/graphiql.min.js"></script>
        <script>
            const graphQLFetcher = graphQLParams =>
                fetch('graphql', {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJleHAiOjE3NTM4NzYzMjJ9.pqWkE2nmrdgp91nnO7kGvQRpBNKqn0BAd42PzQDq18Q'
                    },
                    body: JSON.stringify(graphQLParams),
                })
                .then(response => response.json())
                .catch(() => response.text());
            
            ReactDOM.render(
                React.createElement(GraphiQL, {
                    fetcher: graphQLFetcher,
                }),
                document.getElementById('graphiql'),
            );
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)