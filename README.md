# HTTP QUERY Method Caching Demo

This example demonstrates the conceptual HTTP QUERY method (as discussed in RFC 10008, a placeholder for a new method) and its associated caching challenges. It includes a simple Python HTTP server that implements `do_QUERY` to process requests with a JSON body and an in-memory cache. A client sends various QUERY requests, showing how identical queries result in cache hits and different queries cause cache misses, highlighting the importance of request body content for caching.

## Language

`python`

## How to Run

1. Save the code as `main.py`.
2. Run from your terminal: `python main.py`
3. Observe the server and client output, noting the `X-Cache` headers.

## Original Article

This example accompanies the Turkish article: [HTTP QUERY Metodu (RFC 10008): Yeni Bir Dünya, Yeni Önbellekleme Zorlukları](https://fatihsoysal.com/blog/http-query-metodu-rfc-10008-yeni-bir-dunya-yeni-onbellekleme-zorluklari/).

## License

MIT — see [LICENSE](LICENSE).
